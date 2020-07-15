import time
from collections import OrderedDict
from datetime import datetime

from rest_framework.response import Response
from rest_framework.pagination import CursorPagination, PageNumberPagination

from question.models import Question


class MyAnswerPagination(PageNumberPagination):
    """自定义分页类,回答分页"""
    # 每页默认数量
    page_size = 15
    # 每页最大显示数量
    max_page_size = 20

    # 自定义返回格式
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('results', data),
        ]), )


class MyCommentPagination(CursorPagination):
    """
    自定义分页类( 以添加时间排序的情况)
    评论分页
    """
    # 每页默认数量
    page_size = 1
    # 排序规则
    ordering = '-add_time'
    # 每页最大显示数量
    max_page_size = 20

    # 自定义返回格式
    def get_paginated_response(self, data, hand_pick_commnets):
        return Response({'comment': OrderedDict([
            ('next', self.get_next_link()),
            ('results', data)
        ]), 'hand_pick_commnets': hand_pick_commnets})


class MyRevertPagination(CursorPagination):
    """
    自定义分页类( 以添加时间排序的情况)
    评论分页
    """
    # 每页默认数量
    page_size = 1
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


def add_question_operation_data(operation, coon, question_id):
    """
    为问题添加操作数据
    参数:1.operation(操作类型 'scan':增加浏览量 'answer':增加回答量,
    'approval':(增加赞同量),'attention':(增加关注量), 'comment':(增加评论量))
        2.coon:redis连接
        3.question_id:问题id
    """
    today = time.strftime('%Y%m%d')
    today_time = datetime.now()
    # 添加数据之前先判断该问题今天是不是第一次浏览
    if operation == 'scan':
        question_exists = coon.exists('question:operation:' + str(question_id) + ':' + today)
        # 若redis没有改键,则说明这个问题今天是第一次浏览, 添加各种数据，同时设置过期时间
        if not question_exists:
            question_school_id = Question.objects.filter(pk=question_id).values_list('school_id')
            coon.hmset('question:operation:' + str(question_id) + ':' + today,
                       {'scan': 0, 'answer': 0, 'approval': 0, 'attention': 0, 'comment': 0})
            coon.sadd('question:operation:' + today, question_id)
            coon.zadd('question:hot:' + str(question_school_id[0][0]) + ':' + today, {str(question_id): float(0)})
            # 设置过期时间
            coon.expireat('question:operation:' + str(question_id) + ':' + today,
                          datetime(year=today_time.year, month=today_time.month, day=today_time.day + 1, hour=2,
                                   minute=0, second=0))

            coon.expireat('question:operation:' + today, datetime(year=today_time.year, month=today_time.month,
                                                                  day=today_time.day + 1, hour=2, minute=0, second=0))

            coon.expireat('question:hot:' + str(question_school_id[0][0]) + ':' + today,
                          datetime(year=today_time.year, month=today_time.month, day=today_time.day + 1, hour=2,
                                   minute=0, second=0))
    # 将相应的数据递增1
    coon.hincrby('question:operation:' + str(question_id) + ':' + today, operation, 1)
