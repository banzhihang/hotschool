from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response


class UserAttentionPagination(CursorPagination):
    """用户关注和被关注分页器"""

    # 每页默认数量
    page_size = 20
    # 每页最大显示数量
    max_page_size = 30
    # 排序
    ordering = 'nick_name'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('results', data)
        ]))


class UserCreateByTimePagination(UserAttentionPagination):
    """用户回答,评论，回复，动态( 以添加时间排序的情况)"""

    page_size = 10
    ordering = '-add_time'
    max_page_size = 20


class UserDynamicByTimePagination(UserCreateByTimePagination):
    """用户动态分页器(按时间排序)"""
    pass


class UserCollectPagination(PageNumberPagination):
    """用户收藏分页器(按redis排序)"""
    age_size = 10
    max_page_size = 15

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('results', data)
        ]))


class UserRecentPagination(UserCollectPagination):
    """最近浏览记录分页器(按redis排序)"""
    # 每页默认数量
    page_size = 15
    # 每页最大显示数量
    max_page_size = 20



