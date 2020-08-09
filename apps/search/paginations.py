from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class UserSearchPagination(PageNumberPagination):
    """搜索用户分页器"""

    # 每页默认数量
    page_size = 20
    # 每页最大显示数量
    max_page_size = 30

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('results', data)
        ]))


class FoodSearchPagination(UserSearchPagination):
    """搜索美食分页器"""

    # 每页默认数量
    page_size = 15
    # 每页最大显示数量
    max_page_size = 25


class SchoolSearchPagination(UserSearchPagination):
    """搜索学校分页器"""
    pass


class QuestionSearchPagination(FoodSearchPagination):
    """搜索问题分页器"""
    pass


class FlavourSearchPagination(UserSearchPagination):
    """搜索口味分页器"""
    # 每页默认数量
    page_size = 10
    # 每页最大显示数量
    max_page_size = 15