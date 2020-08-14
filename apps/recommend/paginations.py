from collections import OrderedDict

from rest_framework.pagination import CursorPagination
from rest_framework.response import Response


class RecommentQuestionByTimePagination(CursorPagination):
    """用户关注和被关注分页器"""

    # 每页默认数量
    page_size = 2
    # 每页最大显示数量
    max_page_size = 20
    # 排序
    ordering = 'add_time'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('results', data)
        ]))