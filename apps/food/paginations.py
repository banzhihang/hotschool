from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.pagination import CursorPagination


class FoodByScorePagination(CursorPagination):
    """
    美食排行分页器(score排序)
    """
    # 每页默认数量
    page_size = 10
    # 排序规则
    ordering = '-score'
    # 每页最大显示数量
    max_page_size = 20

    # 自定义返回格式
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('results', data)
        ]), )


class FoodByTimePagination(CursorPagination):
    """
    美食排行分页器(time排序)
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
        ]), )


class ShortCommentByApprovalNumberPagination(CursorPagination):
    """
    美食短评分页器(approval_number排序)
    """
    # 每页默认数量
    page_size = 15
    # 排序规则
    ordering = '-approval_number'
    # 每页最大显示数量
    max_page_size = 25

    # 自定义返回格式
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('results', data)
        ]), )


class ShortCommentByTimePagination(CursorPagination):
    """
    美食短评分页器(time排序)
    """
    # 每页默认数量
    page_size = 15
    # 排序规则
    ordering = '-add_time'
    # 每页最大显示数量
    max_page_size = 25

    # 自定义返回格式
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('results', data)
        ]), )


class DiscussByCommentNumberPagination(CursorPagination):
    """讨论分页器(按评论数排序)"""

    # 每页默认数量
    page_size = 20
    # 排序规则
    ordering = '-approval_number'
    # 每页最大显示数量
    max_page_size = 25

    # 自定义返回格式
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('results', data)
        ]), )


class DiscussByTimePagination(CursorPagination):
    """讨论分页器(按时间排序)"""

    # 每页默认数量
    page_size = 20
    # 排序规则
    ordering = '-add_time'
    # 每页最大显示数量
    max_page_size = 25

    # 自定义返回格式
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('results', data)
        ]), )


class CommentByTimePagination(CursorPagination):
    """评论分页器(按时间排序)"""

    # 每页默认数量
    page_size = 15
    # 排序规则
    ordering = 'add_time'
    # 每页最大显示数量
    max_page_size = 25

    # 自定义返回格式
    def get_paginated_response(self, comment_data,hand_pick_commnets_data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('results', comment_data),
            ('hand_pick_commnets',hand_pick_commnets_data),
        ]), )


class RevertByTimePagination(CursorPagination):
    """回复分页器(按时间排序)"""

    # 每页默认数量
    page_size = 20
    # 排序规则
    ordering = 'add_time'
    # 每页最大显示数量
    max_page_size = 25

    # 自定义返回格式
    def get_paginated_response(self,data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('results', data),
        ]), )