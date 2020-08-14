from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication
from rest_framework_jwt.authentication import jwt_decode_handler
from rest_framework_jwt.utils import jwt_get_user_id_from_payload_handler

from user.models import User


class Authtication(BasicAuthentication):
    """自定义用户认证(必须登录才能访问)"""

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


class LooseAuthtication(BasicAuthentication):
    """宽松的自定义用户认证(不登陆和登录都能访问,但是二者的数据不同)"""

    def authenticate(self, request):
        # 获取token
        token = request.META.get('HTTP_AUTHORIZATION', None)
        # token不存在,该名用户就是游客,返回AnonymousUser
        if token is None:
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