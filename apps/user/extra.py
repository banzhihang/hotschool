import re
from collections import OrderedDict
from io import BytesIO

import redis
import requests
import random, string

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication
from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.response import Response
from rest_framework_jwt.authentication import jwt_decode_handler
from rest_framework_jwt.utils import jwt_get_user_id_from_payload_handler

from user.models import User

POOL = redis.ConnectionPool(host='127.0.0.1', port=6379,db=1,decode_responses=True)

def random_string(slen=30): #截取长度不能超过指定序列的长度
    # 产生随机字符串，当作图片的名字
    return ''.join(random.sample(string.ascii_letters + string.digits + '@#$%&', slen))

def modify_image_name(request):
    # 修改图片的名字，解决了不能上传含有中文名的图片的问题.使用正则表达式匹配图片的content_type,获得图片的格式
    # 使用随机字符串代替原始图片名
    try:
        img_type = request.data.get('head_portrait').content_type
    except:
        return request
    else:
        pattern = re.compile('[^/]+$')
        tail = re.findall(pattern, img_type)
        path = random_string() + '.' + tail[0]
        request.data.get('head_portrait').name = path
        return request


class OpenIdAndImage:
    """获取openid和用户微信头像"""

    def __init__(self, code,image_url):
        self.openid_url = 'https://api.weixin.qq.com/sns/jscode2session'
        # 头像地址
        self.img_url = image_url
        self.app_id = 'wx35df04e950c9cad8'
        self.app_secret = '7107762d645e15f6f49bdfb0e4180aa4'
        self.code = code

    def get_openid_image(self):
        openid_url = self.openid_url + "?appid=" + self.app_id + "&secret=" + self.app_secret +\
                     "&js_code=" + self.code + "&grant_type=authorization_code"
        res1 = requests.get(openid_url)
        res2 = requests.get(self.img_url)
        try:
            openid = res1.json()['openid']
            # 图像内容为二进制格式，要转换成django InMemoryUploadedFile类型
            res3 = res2.content
            image = BytesIO(res3)
            # 改变图片的名字，用正则表达式匹配图像type,使用随机字符串代替原名字
            image_type = res2.headers.get("Content-Type")
            pattern = re.compile('[^/]+$')
            # 获得图像格式
            tail = re.findall(pattern, image_type)
            image = InMemoryUploadedFile(image, None, random_string()
                                         +'.'+tail[0], None, len(res3), None, None)
        except:
            return Response({"msg": "登录失败"})
        else:
            return openid,image


class Authtication(BasicAuthentication):
    """自定义用户认证"""

    def authenticate(self, request):
        # 获取token
        token = request.META.get('HTTP_AUTHORIZATION', None)
        # token不存在
        if token is None:
            raise exceptions.AuthenticationFailed('未登录')
        try:
            # 解析token,若出现异常，则说明token被篡改过，属于非法
            payload = jwt_decode_handler(token)
        except Exception:
            raise exceptions.AuthenticationFailed('用户异常')

        # 获得用户id
        user_id = jwt_get_user_id_from_payload_handler(payload)
        try:
            user = User.objects.get(pk=user_id)
        except Exception:
            raise exceptions.AuthenticationFailed('没有该用户')
        else:
            return user, None


class MyCursorPagination(CursorPagination):
    """自定义分页类( 以添加时间排序的情况)
    用户回答,评论，回复，动态
    """
    # 每页默认数量
    page_size = 10
    # 排序规则
    ordering = '-add_time'
    # 每页最大显示数量
    max_page_size = 20

    # 自定义返回格式
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('results', data)
        ]),)


class RecentPagination(PageNumberPagination):
    """自定义分页类(最近浏览记录)"""
    # 每页默认数量
    page_size = 1
    # 每页最大显示数量
    max_page_size = 50

    # 自定义返回格式
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('results', data)
        ]),)


def get_ordering(answer_id):
    # 生成排序条件
    condition_list = ['WHEN id = % s THEN % s' % (pk, index) for index, pk in enumerate(answer_id)]
    condition = ' '.join(condition_list)
    ordering = 'CASE %s END' % condition

    return ordering