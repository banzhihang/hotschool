import json

from django.test import TestCase

# Create your tests here.
from django_redis import get_redis_connection

# import redis
#
# POOL = redis.ConnectionPool(host='127.0.0.1', port=6379,)
# coon = redis.Redis(connection_pool=POOL)
# # a = {'name': '班治杭', 'age': 18, 'time': '2020'}
# # b = {'name': '奥特曼', 'age': 20, 'time': '2010'}
# # c = {'name': '小朋哟', 'age': 18, 'time': '2050'}
# a = {'v1':10}
# b = {'v2':11}
# c = {'v3':12}
# d = {'v4':13}
# # coon.zadd('user:message:51', {json.dumps(a, ensure_ascii=False): a['time']})
# # coon.zadd('user:message:51', {json.dumps(b, ensure_ascii=False): b['time']})
# # coon.zadd('user:message:51', {json.dumps(c, ensure_ascii=False): c['time']})
# coon.zadd('user:message:51', a)
# coon.zadd('user:message:51', b)
# coon.zadd('user:message:51', c)
# coon.zadd('user:message:51', d)
# x = coon.zrevrank('user:message:51', 'v1')
#
# for i in range(0,4):
#     t = coon.zrevrange('user:message:51',start=x,end=x)
#     t.get()
#     if not t:
#         break
#     print(t[0].decode('utf-8'))
#     x+=1
# m = coon.dbsize()
# print(m)
#
# coon.flushall()
from socket import *
serverName = '192.168.31.202'
serverPort = 12000
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
message = input("请输入：")
clientSocket.send(message.encode())
modifiedMessage = clientSocket.recv(1024)
print(modifiedMessage.decode())