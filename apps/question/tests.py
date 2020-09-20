import json
import re
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

# from socket import *
# serverPort = 12000
# serberSocket = socket(AF_INET,SOCK_STREAM)
# serberSocket.bind(('',serverPort))
# serberSocket.listen(1)
# print('start')
# while True:
#     connectSocket,address =serberSocket.accept()
#     message= connectSocket.recv(1024)
#     modifyMessage = message.decode().upper()
#     print(message,modifyMessage)
#     connectSocket.send(modifyMessage.encode())
#     connectSocket.close()
from datetime import datetime,timedelta
import time
# now = datetime.datetime.now()
# a = time.mktime(now.timetuple())
# print(a,type(a))
# now_time = time.mktime(now.timetuple())
# print(now_time)
# after_hour = datetime.now() + timedelta(hours=1)
# print(after_hour)
# after_timestamp = time.mktime(after_hour.timetuple())
# print(after_timestamp,type(after_timestamp))
# from communicate.tests import coon
# dynamic = {'type':1,'answer':1,'user':1}
# coon.zadd('dynamic:1',{json.dumps(dynamic,ensure_ascii=False):1.2})
# dynamic_exist = coon.zrank('dynamic:1',json.dumps(dynamic,ensure_ascii=False))
# print(dynamic_exist)
# def search( nums, target: int) -> int:
#     if not nums:
#         return -1
#     l, r = 0, len(nums) - 1
#     while l <= r:
#         mid = (l + r) // 2
#         if nums[mid] == target:
#             return mid
#         if nums[0] <= nums[mid]:
#             if nums[0] <= target < nums[mid]:
#                 r = mid - 1
#             else:
#                 l = mid + 1
#         else:
#             if nums[mid] < target <= nums[len(nums) - 1]:
#                 l = mid + 1
#             else:
#                 r = mid - 1
#     return -1
#
#
# a = search([4,5,6,7,-1,0,1,2,3],0)
# print(a)
# import redis
#
# POOL = redis.ConnectionPool(host='127.0.0.1', port=6379,db=1,decode_responses=True)
#
# coon = redis.Redis(connection_pool=POOL)
# x = ['approval','vote']
# a = coon.hmget('ad:1',*x)
# print(a)


# # 查询问题的在榜记录，若问题在该zset中，则该问题不能上榜
# hot_question_record_list = coon.zrange('hot:record:' + str(school_id), start=0, end=-1)
# # 集和求交集，求出哪些问题最近上过热榜
# record = set(hot_question_id_list) & set(hot_question_record_list)
# count = 0
# # 去除最近在榜过的问题id(将该问题的id移动到排行列表的末尾)
# if record:
#     for i in record:
#         # 将限定时间内上榜过的问题id添加到列表末尾
#         hot_question_id_list.remove(i)
#         hot_question_id_list.append(i)
#         count += 1

# expire_time = (datetime.now()+timedelta(days=2)).timestamp()
# expire_time1 = datetime.now().timestamp()
# print(expire_time,expire_time1)
import redis
#
from bs4 import BeautifulSoup

POOL = redis.ConnectionPool(host='127.0.0.1', port=6379,db=1,decode_responses=True)
#
#
# now_timestamp = time.time()
# coon = redis.Redis(connection_pool=POOL)
# a=coon.zscore('answer:score:2',1)
# print(a)
# hot_record_list = coon.zrange('hot:record:0', start=0, end=-1, withscores=True)
# print(hot_record_list)
# tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
# expireat_time = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 3, 0, 0)
# # 设置过期时间。redis key过期时间为第二天半夜3点
# coon.expireat('qd:' + str(question_id) + ':' + today, expireat_time)


# coon = redis.Redis(connection_pool=POOL)
# school_id = 1
# today = datetime.now().strftime('%Y%m%d')
# # 热榜问题的过期时间
# expire_time = (datetime.now() + timedelta(days=2)).timestamp()
# # 热榜问题前15
# hot_list = coon.zrevrange('hot:' + str(school_id) + ':' + today, start=0, end=14)
# dict = {}
# # 构造字典,键为前二十问题id,值为2天之后的时间戳
# for i in hot_list:
#     dict[i] = expire_time
# # 将这些问题添加到热榜记录
# coon.zadd('hot:record',dict)
# zset_number = coon.zcard('hot:' + str(school_id) + ':' + today)
# if zset_number <=15:
#     pass
# else:
# # 将该学校的热榜除了前15全部删除
#     coon.zremrangebyrank('hot:' + str(school_id) + ':' + today,min=0,max=zset_number-15-1)


# def get(self, request):
#     """
#     获取问题详情
#     参数:question_id,type(排序条件)
#     """
#     try:
#         question_id = request.GET.get('question')
#         answer_type = int(request.GET.get('type', 0))
#         page = request.GET.get('page')
#         coon = redis.Redis(connection_pool=POOL)
#         #  若type为0,则为默认排序，为1则为按发布时间排序,从redis获取排名
#         if int(answer_type) == 0:
#             answer_id = coon.zrevrange('answer:score:' + str(question_id), start=0, end=-1)
#         else:
#             answer_id = coon.zrevrange('answer:time:' + str(question_id), start=0, end=-1)
#
#         # 获得排名之后生成去数据库按顺序查询
#         ordering = get_ordering(answer_id)
#         answers_set = Answer.objects.filter(question_id=question_id).only('id', 'user', 'modify_time', 'content',
#                                                                           'approval_number', 'comment_number',
#                                                                           'like_number').extra(
#             select={'ordering': ordering}, order_by=('ordering',))
#
#     except Exception:
#         return Response({'next': '', 'error': '发生错误', 'results': ''})
#     else:
#         # 将该问题的浏览量加1
#         add_question_operation_data('scan', question_id)
#         if answer_id:
#             pages = MyAnswerPagination()
#             page_roles = pages.paginate_queryset(queryset=answers_set, request=request, view=self)
#             answers = AnswerBriefSerializer(instance=page_roles, many=True, context={'request': request})
#         else:
#
#         if not page:
#             question_set = Question.objects.get(pk=question_id)
#             question = QuestionInfoSerializer(instance=question_set, many=False, context={'request': request})
#             return pages.get_paginated_response(question.data, answers.data)
#         else:
#             return pages.get_paginated_response('null', answers.data)
#
#
# [
#             ('next', self.get_next_link()),
#             ('error', ''),
#             ('question', question_data),
#             ('answer', answer_data),
#         ]

# coon = redis.Redis(connection_pool=POOL)
# a = coon.zrange('a',start=0,end=-1)
# print(a)

import html
# s = '''
# <p>让我日群无若无群若热无群若无温热群热情无若而我却若犬瘟热玩儿请问</p><p>wrwriworiw</p><p>你好啊啊</p><p><img src="http://img1.3lian.com/2015/w7/85/d/101.jpg" data-custom='id=imgage'></p><p><br></p>
# '''
# def test(html):
#     pattern = re.compile('img src="(.*?)"')
#     # 获得第一张图片
#     img_url = pattern.search(html)
#     # 获得回答摘要
#     clean_text = BeautifulSoup(html, "lxml").get_text(strip=True)
#
#     print(img_url[1],clean_text)
#
# test(s)

