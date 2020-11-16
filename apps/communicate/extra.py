import json,time

import redis
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_jwt.authentication import jwt_decode_handler
from rest_framework_jwt.utils import jwt_get_user_id_from_payload_handler
from channels.layers import get_channel_layer

from HotSchool.settings import POOL
from user.models import User


class QueryAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        # 关闭旧的链接
        close_old_connections()
        return QueryAuthMiddlewareInstance(scope, self)


class QueryAuthMiddlewareInstance:
    """Inner class that is instantiated once per scope."""
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        self.scope['user'] = await get_user(self.scope)
        # Instantiate our inner application
        inner = self.inner(self.scope)

        return await inner(receive, send)


@database_sync_to_async
def get_user(scope):
    """将数据库访问变成异步的"""
    try:
        token = str(scope['query_string'].decode('utf-8'))
    except Exception:
        token = None

    # 如果没有token,则返回AnonymousUser()
    if not token:
        user = AnonymousUser()
        return user
    else:
        try:
            # 解析token,若出现异常，则说明token被篡改过，属于非法,将该连接的user置为AnonymousUser,channel将会拒绝该websocket连接
            payload = jwt_decode_handler(token)
        except Exception:
            user = AnonymousUser()
            return user
        else:
            # 获得用户id
            user_id = jwt_get_user_id_from_payload_handler(payload)
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                user = AnonymousUser()
            return user


def notification_user(to_user,data):
    """获取用户的channel,向用户发送通知"""
    # 获取通道层
    channel_layer = get_channel_layer()
    # 该推送消息的时间戳
    now_time = time.time()
    coon = redis.Redis(connection_pool=POOL)
    # 获取接收者的通道名
    to_user_channel_name = coon.hget('user:connect',str(to_user))
    # 将消息发送到对应套接字的通道
    if to_user_channel_name:
        # 通道层只支持异步,需要使用async_to_sync将异步方法转为同步方法
         async_to_sync(channel_layer.send)(
            to_user_channel_name,
            {
                'type':'chat_message',
                'data':data
            })
    # 若用户不在线，将消息存入redis中暂存
    else:
        coon.zadd('message:' + str(to_user), {
            json.dumps(data, ensure_ascii=False): float(now_time)})

