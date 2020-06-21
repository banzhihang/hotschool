from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_jwt.authentication import jwt_decode_handler
from rest_framework_jwt.utils import jwt_get_user_id_from_payload_handler

from user.models import User


class QueryAuthMiddleware:
    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):
        close_old_connections()
        Jwt = JwtAuthentication(scope)
        user = Jwt.get_user()

        return self.inner(dict(scope, user=user))


class JwtAuthentication:
    """自定义websocket认证"""
    def __init__(self,scope):
        # 获取token
        try:
            self.token = str(scope['query_string'].decode('utf-8'))
        except Exception:
            self.token = None

    def get_user(self):
        """获取用户"""
        if self.token is None:
            user = AnonymousUser()
            return user
        try:
            # 解析token,若出现异常，则说明token被篡改过，属于非法
            payload = jwt_decode_handler(self.token)
        except Exception:
            user = AnonymousUser()
            return user
        else:
            # 获得用户id
            user_id = jwt_get_user_id_from_payload_handler(payload)
            try:
                user = User.objects.get(pk=user_id)
            except Exception:
                user = AnonymousUser()
            return user
