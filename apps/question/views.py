import json
from datetime import date

from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from . import tasks
from .logics import *
from .serializers import QuestionInfoSerializer, AnswerInfoSerializer


class JsonToDatetime(json.JSONEncoder):
    """处理json datetime数据"""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


class HotQuestionView(View):
    """获取热门内容
    参数：campus(校区),college(学院),time(0(24小时),1(一周))
    返回值：热门内容列表
    """

    def get(self, request):
        campus = request.GET.get('campus', None)
        college = request.GET.get('college', None)
        time_slot_type = int(request.GET.get('time', 0))

        questions = get_hot_question(campus, college, time_slot_type)

        data = {
            'errorcode': 0,
            'questions': questions
        }

        return HttpResponse(json.dumps(data, cls=JsonToDatetime))


class AQuestionView(APIView):
    """获取问题详情
    参数：question_id,type(0为回答默认排序,1为回答按时间排序)
    返回值：回答列表
    """

    def get(self, request, question_id):
        answer_type = int(request.GET.get('type', 0))
        question, answers = get_question_info(question_id, answer_type)
        # 异步处理添加浏览记录到热榜操作表
        tasks.add_user_browse.delay(question_id=question_id, type=0)

        questions = QuestionInfoSerializer(instance=question, many=False)
        answers = AnswerInfoSerializer(instance=answers, many=True)

        return Response({'questions': questions.data, 'answers': answers.data})


class CommentView(View):
    """
    获取用户评论
    参数：answer_id,question_id,comment_type
    返回值：comments
    """

    def get(self, request):
        answer_id = request.GET.get('answer_id', '')
        question_id = request.GET.get('question_id', '')
        comment_type = request.GET.get('type', '')

        comments = get_comment(answer_id, comment_type, question_id)

        data = {
            'comments': comments,
        }

        return HttpResponse(json.dumps(data, cls=JsonToDatetime))


class RevertView(View):
    """获取用户回复
    参数：comment_id
    返回值：用户回复
    """

    def get(self, request):
        comment_id = request.GET.get('comment_id', '')
        reverts = get_revert(comment_id)

        data = {
            'reverts': reverts,
        }

        return HttpResponse(json.dumps(data, cls=JsonToDatetime))
