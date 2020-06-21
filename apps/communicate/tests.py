import json

from django.test import TestCase

# Create your tests here.
from django_redis import get_redis_connection

import redis

POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, )
coon = redis.Redis(connection_pool=POOL)
a = {'name': '班治杭', 'age': 18, 'time': '2020'}
b = {'name': '奥特曼', 'age': 20, 'time': '2010'}
c = {'name': '小朋哟', 'age': 18, 'time': '2050'}
coon.zadd('user:message:51', {json.dumps(a, ensure_ascii=False): a['time']})
coon.zadd('user:message:51', {json.dumps(b, ensure_ascii=False): b['time']})
coon.zadd('user:message:51', {json.dumps(c, ensure_ascii=False): c['time']})
c = coon.zrange('user:message:51', start=0, end=-1)

for i in c:
    print(i.decode())
coon.flushall()
