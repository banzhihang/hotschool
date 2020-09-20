from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.pagination import CursorPagination, PageNumberPagination


class RevertByTimePagination(CursorPagination):
    """回复分页(以添加时间排序的情况)"""

    # 每页默认数量
    page_size = 25
    # 排序规则
    ordering = 'add_time'
    # 每页最大显示数量
    max_page_size = 30

    # 自定义返回格式
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('results', data)
        ]), )


class CommentByTimePagination(RevertByTimePagination):
    """评论分页(以添加时间排序的情况)"""

    def get_paginated_response(self, data, hand_pick_commnets):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('results', data),
            ('hand_pick_commnets', hand_pick_commnets)
        ]))


class AnswerPagination(PageNumberPagination):
    """回答分页(按照redis排序)"""

    page_size = 10
    max_page_size = 15

    def get_paginated_response(self,question_data, answer_data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('question', question_data),
            ('answer', answer_data),
        ]), )


class CollectCommentByTimePagination(CursorPagination):
    """我的发布中评论详情分页器"""

    # 每页默认数量
    page_size = 15
    # 排序规则
    ordering = 'add_time'
    # 每页最大显示数量
    max_page_size = 25

    def get_paginated_response(self,comment_data, revert_data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('comment', comment_data),
            ('revert', revert_data),
        ]), )