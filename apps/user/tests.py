#
# from django.test import TestCase
# import requests
# from PIL import Image
# from io import BytesIO
# import re
#
# from django.core.files.uploadedfile import InMemoryUploadedFile
#
# # img_url = 'https://wx.qlogo.cn/mmopen/vi_32/E2L7eCcteRTnqE6klRT4tcTNYUb2arB7iaicQdlHQuHUcryJezXbtptggsxnWZSqg4AernyGEMSic7iaXoVicdkDJyA/132'
# # # res2 = requests.get(img_url)
# # #
# # # a=res2.content
# # # tail = res2.headers.get("Content-Type")
# # # pattern = re.compile('[^/]+$')
# # # b=re.findall(pattern,tail)
# # # print(tail)
# # # bytes_stream = BytesIO(a)
# # # image = InMemoryUploadedFile(bytes_stream, None, 'aa'+'.'+b[0], None, len(a), None, None)
# # # print(1)
#
# # a = '"娱乐,美女"'
# # list = a.strip(";").split(',')
# # #pattern = re.compile('^[^"]*[^"]$')
# # #interests = re.findall(pattern,a)[0]
# # print(list)
# # print(type(list))
#
# a = {'a':22}
# b = a.get('b')
# print(b)
#
#
#
#
#
#     add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
#     answer = serializers.IntegerField(source='answer.id')
#     user_nick_name = serializers.CharField(source='answer.user.nick_name')
#     approval_number = serializers.IntegerField(source='answer.approval_number')
#     comment_number = serializers.IntegerField(source='answer.comment_number')
#     question_title = serializers.CharField(source='answer.question.title')
#
#     class Meta:
#         model = RecentBrowseAnswer
#         fields = ['add_time', 'answer','user_nick_name','approval_number',
#                   'comment_number','question_title']

# from django_redis import get_redis_connection
#
# coon = get_redis_connection()
# coon.hset('user','user1','15')
# coon.hset('user','user2','15')
# coon.hset('book','price','1259')
#
# a = coon.hget('user','user1')
# b = coon.hget('user','user2')
# c = coon.hget('book','price','1259')
#
# coon.hdel('user','user1')
# coon.hdel('user','user2')
# coon.hdel('book','price')

# from socket import *
# serverName = '192.168.31.202'
# serverPort = 12000
# clientSocket = socket(AF_INET,SOCK_STREAM)
# clientSocket.connect((serverName,serverPort))
# message = input("请输入：")
# clientSocket.send(message.encode())
# modifiedMessage = clientSocket.recv(1024)
# print(modifiedMessage.decode())
# def multiply( A: int, B: int) -> int:
#     if B == 0:
#         return 0
#     if A < B:
#         A, B = B, A
#     else:
#         return A + multiply(A, B - 1)
#
# print(multiply(1,10))
# import time
# import uuid
# time_str  = str(time.time())
# a = uuid.uuid3(uuid.NAMESPACE_DNS,time_str)
# print(str(a))
# print(str(a).replace('-',''))

# def twoSum( nums, target: int):
#     for i in range(len(nums)):
#         a = list(nums)
#         a.remove(nums[i])
#         for j in range(len(a)):
#             if nums[i] + a[j] == target:
#                 k = nums.index(a[j])
#                 return [i, k]
#
# print(twoSum([3,3],6))
# import redis
#
import time
import redis

from question.algorithms import calculate_question_hot_score

POOL = redis.ConnectionPool(host='127.0.0.1', port=6379,db=1,decode_responses=True)
# coon = redis.Redis(connection_pool=POOL)
# a = coon.exists('ad:1')
# print(a)

# from datetime import datetime,timedelta
# yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
# print(yesterday)



# def check_hot_question_expire_time():
# #     """定时清理已达到过期时间的上过热榜的问题"""
# #     coon = redis.Redis(connection_pool=POOL)
# #     # 现在的时间戳
# #     now_timestamp = time.time()
# #     # 获得热榜记录的列表(返回示例,元组内部第一个元素为id,第二个元素为过期时间[('2', 11.0), ('1', 1235.0)])
# #     hot_record_list = coon.zrange('hot:record',start=0,end=-1,withscores=True)
# #     delete_list = []
# #     for i in hot_record_list:
# #         # 若过期时间小于现在的时间,就删除
# #         if i[1] <= now_timestamp:
# #             delete_list.append(i[0])
# #     coon.zrem('hot:record',*delete_list)
# #
# #
# # check_hot_question_expire_time()

# from datetime import datetime,timedelta
# def calculate_question_and_syn(question_id):
#     """
#     计算问题的热度值,并将相关数据同步至数据库
#     参数:question_id(问题id)
#     执行时间:第二天半夜2点
#     """
#     yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')  # 昨天的时间字符串
#     coon = redis.Redis(connection_pool=POOL)
#     # 获取问题数据
#     question_data = coon.hmget('qd:'+str(question_id)+':'+yesterday,'scan','answer','approval','attention','comment',
#                                'collect','school')
#     school_id = question_data[6]
#     # 获得上榜问题记录
#     hot_record_list = coon.zrange('hot:record:',start=0,end=-1)
#
#     # 只有不在该学校的热榜上的问题才能上榜
#     if str(question_id) not in hot_record_list:
#         today = datetime.now().strftime('%Y%m%d')
#         # 上榜问题的下一次能上榜限制时间
#         expire_time = (datetime.now() + timedelta(days=2)).timestamp()
#         scan_num,answer_num,approval_num,attention_num,comment_num,collect_num = question_data[0],question_data[1],question_data[2],question_data[3],question_data[4],question_data[5]
#         score = calculate_question_hot_score(scan_num,answer_num,approval_num,attention_num,collect_num,collect_num)
#         # 将该问题添加到问题对应学校的热榜zset
#         coon.zadd('hot:'+str(school_id)+':'+today,{question_id:score})
#         # 将该问题添加到上榜记录
#         coon.zadd('hot:record:',{question_id:expire_time})
#     # # 无论问题是否上榜,都同步数据到数据库
#     # try:
#     #     Question.objects.filter(pk=question_id).update(
#     #         attention_number=F('attention_number')+attention_num,
#     #         scan_number=F('scan_number')+scan_num,
#     #     )
#     # except:
#     #     pass
#     # # 删除该问题留存在redis中的数据
#     coon.delete('qd:'+str(question_id)+':'+yesterday)
#
# calculate_question_and_syn(1)
coon = redis.Redis(connection_pool=POOL)
answer_id = coon.zrange('answer:score:2',start=100,end=100)
print(answer_id)
