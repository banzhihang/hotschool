from collections import OrderedDict

from rest_framework.pagination import CursorPagination
from rest_framework.response import Response


class AnswerDraftByTimePagination(CursorPagination):
    """回答草稿分页(以修改时间排序的情况)"""

    # 每页默认数量
    page_size = 10
    # 排序规则
    ordering = '-modify_time'
    # 每页最大显示数量
    max_page_size = 11

    # 自定义返回格式
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('results', data)
        ]), )


class FoodDraftByTimePagination(AnswerDraftByTimePagination):
    """食物草稿分页器(按修改时间排序)"""
    pass