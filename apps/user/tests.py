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

from django_redis import get_redis_connection

coon = get_redis_connection()
coon.hset('user','user1','15')
coon.hset('user','user2','15')
coon.hset('book','price','1259')

a = coon.hget('user','user1')
b = coon.hget('user','user2')
c = coon.hget('book','price','1259')

coon.hdel('user','user1')
coon.hdel('user','user2')
coon.hdel('book','price')
