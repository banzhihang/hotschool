from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework_jwt.authentication import jwt_decode_handler
from rest_framework_jwt.utils import jwt_get_user_id_from_payload_handler

from user.models import User


class Authtication(BasicAuthentication):
    """自定义用户认证(必须登录才能访问)"""

    def authenticate(self, request):
        # 获取token
        token = request.META.get('HTTP_AUTHORIZATION', None)
        # token不存在
        if not token:
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


class LooseAuthtication(BasicAuthentication):
    """宽松的自定义用户认证(不登陆和登录都能访问,但是二者的数据不同)"""

    def authenticate(self, request):
        # 获取token
        token = request.META.get('HTTP_AUTHORIZATION', None)
        # token不存在,该名用户就是游客,返回AnonymousUser
        if not token:
            return AnonymousUser(), None
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


def get_ordering(id_list):
    # 生成排序条件
    condition_list = ['WHEN id = % s THEN % s' % (pk, index) for index, pk in enumerate(id_list)]
    condition = ' '.join(condition_list)
    ordering = 'CASE %s END' % condition

    return ordering


def verify_view(func):
    """校验用户是否登录的装饰器(用户view class装饰post,put,delete方法)"""
    def wraper(self,request,*args,**kwargs):
        user = request.user
        if not isinstance(user, AnonymousUser):
            return func(self,request,*args,**kwargs)
        # 若用户未登录,直接返回
        else:
            return Response({'status': 'fail', 'error': '未登录'})
    return wraper


def verify_serializers(type=0):
    """
    校验序列化器用户是否登录,从而返回不同数据
    参数:type 若用户未登录返回什么数据
    """
    def wrapper(func):
        def real(self,obj,*args,**kwargs):
            user = self.context['request'].user
            # 若用户用户登录
            if not isinstance(user, AnonymousUser):
                # 将校验过的用户传入
                return func(self,obj,user,*args,**kwargs)
            # 若用户未登录,直接返回需要展示的默认数值
            else: return type
        return real
    return wrapper


def check_undefined(func):
    """检查get请求中是否有undefined,有就直接返回错误"""
    def wrapper(self,request,*args,**kwargs):
        for value in request.GET.values():
            if value == 'undefined':
                return Response('参数错误')
        return func(self,request,*args,**kwargs)
    return wrapper
