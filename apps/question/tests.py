from datetime import datetime,timedelta
import time
# a = time.strftime('%Y%m%d')
# print (a)

# a = set([])
# b = set([5,6,8,2])
# c= a & b
# if c:
#     print('hello')
# else:
#     print('hi')

# time11 = datetime.now().day
# print(time11)
# extime = datetime(2015,9,8,15,19,10)
# extime2=datetime(2015,9,time11+1,15,19,10)
# print(extime)
# print(extime2)
# print(time1)
# print(time1+timedelta(hours=1))
# print(type(time1))
# a = datetime.now()
# year,month,day = a.year,a.month,a.day
# print(datetime(year=year,month=month,day=day+1,hour=2,minute=0,second=0))
# import redis
#
# POOL = redis.ConnectionPool(host='127.0.0.1', port=6379,db=1,decode_responses=True)
# coon = redis.Redis(connection_pool=POOL)
# today = time.strftime('%Y%m%d')
# #path = 'question:operation:2:20200710'
# b = 'question:operation:' + str(2)+ ':'+ today
# a = coon.exists('question:operation:' + str(2)+ ':'+ today)
# print(a)

from socket import *
serverPort = 12000
serberSocket = socket(AF_INET,SOCK_STREAM)
serberSocket.bind(('',serverPort))
serberSocket.listen(1)
print('start')
while True:
    connectSocket,address =serberSocket.accept()
    message= connectSocket.recv(1024)
    modifyMessage = message.decode().upper()
    print(message,modifyMessage)
    connectSocket.send(modifyMessage.encode())
    connectSocket.close()