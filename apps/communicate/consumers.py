import json

from django.contrib.auth.models import AnonymousUser
from django_redis import get_redis_connection
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    """消费者类"""
    async def connect(self):
        # 连接请求
        user = self.scope['user']
        # 禁止未登录用户连接，若用户已经登录，则将用户的channel_name存入redis,方便其他用户判断该用户是否在线
        if type(user) is AnonymousUser:
            pass
        else:
            coon = get_redis_connection()
            coon.set('user:connect:'+str(user.id),self.channel_name)
            await self.accept()
            # 从redis的有序集合中取出所有该用户的离线消息,若存在就推送离线消息
            message_json = coon.zrange('user:message:unread:' + str(user.id),start=0,end=-1)
            if message_json :
                for i in message_json:
                    data = json.loads(i)
                    await self.channel_layer.send(
                        self.channel_name,{
                            'type':'chat_message',
                            'data':data,
                        }
                    )
                coon.delete('user:message:unread:'+str(user.id))

    async def disconnect(self, close_code):
        # 断开连接，同时从redis中删除该用户的channel_name
        user = self.scope['user']
        if type(user) is not AnonymousUser:
            coon = get_redis_connection()
            coon.delete('user:connect:'+str(user.id))

    async def receive(self, text_data):
        # 处理从websocket收到的消息
        text_data_json = json.loads(text_data)
        from_user = self.scope['user'].id
        to_user = text_data_json['to_user']
        time = text_data_json['time']
        message = text_data_json['message']
        # 封装消息发送给channel
        data = {'from_user':from_user,'message':message,'time':time}

        # 判断用户是否在线，在线就直接发送消息，不在线就将消息存入redis的有序集合中,有序集和的排序根据时间戳排序
        coon = get_redis_connection()
        to_user_channel_name = coon.get('user:connect:'+str(to_user))
        if to_user_channel_name :
            await self.channel_layer.send(
                to_user_channel_name.decode(),
                {
                    'type':'chat_message',
                    'data':data,
                }
            )
        else:
            coon.zadd('user:message:unread:'+str(to_user),{
                json.dumps(data,ensure_ascii=False):float(time)})

    async def chat_message(self,event):
        #  处理从channel_layer收到的其他人的消息
        data = event['data']
        message = data['message']
        from_user = data['from_user']
        time = data['time']

        # 将消息发送给websocket(已经指定channel)
        await self.send(text_data=json.dumps({
            'message' : message,
            'from_user':from_user,
            'time':time,
        },ensure_ascii=False))
