import json
import time

import redis
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
# from socket import *
# serverName = '192.168.31.202'
# serverPort = 12000
# clientSocket = socket(AF_INET,SOCK_STREAM)
# clientSocket.connect((serverName,serverPort))
# message = input("请输入：")
# clientSocket.send(message.encode())
# modifiedMessage = clientSocket.recv(1024)
# print(modifiedMessage.decode())

# import datetime
# delta = datetime.timedelta(days=1)
# b = datetime.datetime.now() +delta
# a = datetime.datetime(b.year,b.month,b.day,2,0,0)
# #print(delta)
# #a = datetime.datetime.now().date()
# # b = datetime.datetime(2019,5,31,15,26,15)
# # print(b)
# #print(type(b))
# print(a)
# #print(type(a))
from datetime import datetime, timedelta

# tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
# a = datetime.datetime(tomorrow.year,tomorrow.month,tomorrow.day,2,0,0)
# print(a)

# today_hour =datetime.now()-timedelta(days=1)
# a = today_hour.strftime('%Y%m%d')
# today = yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
# print(today)
# print(type(today))
# print(today_hour.strftime('%Y%m%d'))
# import redis
#
# POOL = redis.ConnectionPool(host='127.0.0.1', port=6379,db=1,decode_responses=True)
#
# coon = redis.Redis(connection_pool=POOL)
# coon.zadd('xxxx',{'boy':1.5})
# a = coon.zrem('xxxx','boy')
# print(a)

# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None
#
#
# class ListTable:
#     def __init__(self):
#         self.head = ListNode(None)
#
#     def add(self,data):
#         node = ListNode(data)
#         if self.head.next is None:
#             self.head.next = node
#         else:
#             cur = self.head
#             while cur:
#                 cur = cur.next
#                 if cur.next is None:
#                     cur.next = node
#                     break
#
#     def show(self):
#         cur = self.head.next
#         while cur:
#             print(cur.val)
#             cur = cur.next
#
#
#
#
#
# def removeElements(head: ListNode, val: int) -> ListNode:
#     cur = head
#     while cur:
#         pre = cur
#         cur = cur.next
#         if cur is None:
#             break
#         if cur.val == val:
#             pre.next = cur.next
#             cur = cur.next
#
#     return head
#
# listtable = ListTable()
# for i in [1,2,6,3,4,5,6]:
#     listtable.add(i)
# a = removeElements(listtable.head,1)
#
# while True:
#     a = a.next
#     print(a.val)
#     if a.next is None:
#         break

# def boy(type,user,question):
#     print(type,question,user)
#
# POOL = redis.ConnectionPool(host='127.0.0.1', port=6379,db=1,decode_responses=True)
# coon = redis.Redis(connection_pool=POOL)
# a = {'type':4,'question':1000,'user':2}
# #coon.zadd('dynamic:2',{json.dumps(a,ensure_ascii=False):1595143932.3572233})
# boy(**a)

# def fib( n: int) -> int:
#     if n < 2: return 1 if n else 0
#     x, y = 0, 1
#     for _ in range(n - 1):
#         x, y = y, x + y
#     return y
#
#
# print(fib(45))
# POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, db=1, decode_responses=True)
#
# coon = redis.Redis(connection_pool=POOL)
# a = coon.hset('user:connect',str(1),'vv')
#
# print(a)
