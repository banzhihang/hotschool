import time

import redis
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.cache.decorators import cache_response

from user.extra import POOL, get_ordering, Authtication
from .extra import MyAnswerPagination, MyCommentPagination, MyRevertPagination, add_question_operation_data
from .models import *
from .serializers import AnswerInfoSerializer, AnswerBriefSerializer, CommentInfoSerializer, RevertInfoSerializer, \
    HotQuestionSerializer


class HotQuestionView(APIView):
    """热门问题视图"""
    @cache_response(60*60) # 添加缓存(60分钟)
    def get(self, request):
        """获取热榜问题"""
        school_id = request.GET('school', 0)
        coon = redis.Redis(connection_pool=POOL)
        today = time.strftime('%Y%m%d')
        # 以当天日期，例如(20200709)为key去redis查询热榜问题的排名
        hot_question_id_list = coon.zrevrange('question:hot:'+str(school_id)+':'+today,start=0,end=60)
        # 查询问题的在榜记录，若问题在该zset中，则该问题不能上榜
        hot_question_record_list = coon.zrange('question:hot:record:'+str(school_id),start=0,end=-1)
        # 集和就交集，求出哪些问题最近上过热榜
        record = set(hot_question_id_list) & set(hot_question_record_list)
        # 去除最近在榜过的问题id(将该问题的id移动到排行列表的末尾)
        if record:
            count = 0
            for i in record:
                # 将限定时间内上榜过的问题id添加到列表末尾
                hot_question_id_list.remove(i)
                hot_question_id_list.append(i)
                count += 1
        # 构造排序条件，以redis给出的顺序去数据库查找问题
        ordering = get_ordering(hot_question_id_list)
        # 若长度大于30,需要截取前30个当作热榜问题
        if len(hot_question_id_list)-count >= 30:
            hot_question_set = Question.objects.all().only('title','id').extra(
                select={'ordering': ordering}, order_by=('ordering',))[0:30]
        else:
            # 若长度不足30个，则需要去除query_set最后几个最近已经上过热榜的问题
            query_length = len(hot_question_id_list) - count
            hot_question_set = Question.objects.all().only('title','id').extra(
                select={'ordering': ordering}, order_by=('ordering',))[0:query_length]

        hot_question = HotQuestionSerializer(instance=hot_question_set,many=True,context={'request': request})

        return Response(hot_question.data)


class QuestionView(APIView):
    """问题视图"""
    def get(self, request, question_id):
        """
        获取问题详情
        参数:question_id,type(排序条件)
        """
        answer_type = request.GET.get('type', 0)
        coon = redis.Redis(connection_pool=POOL)
        # 将该问题的浏览量加1
        add_question_operation_data('scan',coon,question_id)
        #  若type为0,则为默认排序，为1则为按发布时间排序,从redis获取排名
        if int(answer_type) == 0:
            answer_id = coon.zrevrange('question:answer:rank:score:' + str(question_id), start=0, end=-1)
        else:
            answer_id = coon.zrevrange('question:answer:rank:time:' + str(question_id), start=0, end=-1)

        # 获得排名之后生成去数据库按顺序查询
        ordering = get_ordering(answer_id)
        answers_set = Answer.objects.filter(question_id=question_id).only('id', 'user', 'modify_time', 'content',
                                                            'approval_number', 'comment_number','like_number').extra(
                                                        select={'ordering': ordering}, order_by=('ordering',))
        page = MyAnswerPagination()
        page_roles = page.paginate_queryset(queryset=answers_set, request=request, view=self)
        answers = AnswerBriefSerializer(instance=page_roles, many=True, context={'request': request})

        return page.get_paginated_response(answers.data)


class AnswerView(APIView):
    """回答视图"""
    authentication_classes = [Authtication, ]

    def get(self, request, answer_id):
        """
        获取回答详情
        参数:answer_id,type(0为默认排序,1为时间排序)
        """
        type = request.GET.get('type',0)
        answer_set = Answer.objects.get(pk=answer_id)
        question = answer_set.question_id
        answer = AnswerInfoSerializer(instance=answer_set, many=False, context={'request': request})
        # 去redis 获取该回答的排名，并根据该回答的排名获取下一个回答的id, 返回给前端
        coon = redis.Redis(connection_pool=POOL)
        # type为0,为默认排序,为 1则为时间排序
        if int(type) == 0:
            index = coon.zrevrank('question:answer:rank:score:'+str(question), str(answer_id))
            next_answer_list = coon.zrevrange('question:answer:rank:score:' + str(question), start=index + 1, end=index + 1)
        else:
            index = coon.zrevrank('question:answer:rank:time:'+str(question), str(answer_id))
            next_answer_list = coon.zrevrange('question:answer:rank:time:'+str(question), start=index + 1,end=index + 1)

        # redis的zrevrange方法返回的是一个列表
        if next_answer_list:
            next_answer = int(next_answer_list[0])
        # 若next_answer_list为None ，则说明为最后一个问题,next_answer就为null
        else:
            next_answer = 'null'

        return Response({'answer': answer.data, 'next': next_answer})

    def delete(self,request):
        """ 删除回答"""


class CommentView(APIView):
    """回答或者问题评论视图"""
    authentication_classes = [Authtication, ]

    def get(self, request):
        """
        获取回答或者问题的评论
        参数：answer_id或者question_id,分页的话，还有cursor
        """
        answer_id = request.GET.get('answer')
        question_id = request.GET.get('question')
        cursor = request.GET.get('cursor')

        if answer_id:
            type = 1
            comment_set = Comment.objects.filter(answer=answer_id,type=1)
        elif question_id:
            type = 0
            comment_set = Comment.objects.filter(answer=question_id, type=0)

        page = MyCommentPagination()
        page_roles = page.paginate_queryset(queryset=comment_set, request=request, view=self)
        comments = CommentInfoSerializer(instance=page_roles, many=True, context={'request': request})

        # 若cursor为None,则说明是请求下一页评论,而非第一次加载评论
        if not cursor:
            if type == 1:
                hand_pick_commnets_set = Comment.objects.filter(answer=answer_id, type=1).order_by('-approval_number')
            else:
                hand_pick_commnets_set = Comment.objects.filter(answer=answer_id, type=0).order_by('-approval_number')
            # 精选评论只有5条
            if hand_pick_commnets_set.count() >= 5:
                hand_pick_commnets_set = hand_pick_commnets_set[0:5]

            hand_pick_commnets = CommentInfoSerializer(instance=hand_pick_commnets_set, many=True,context={'request': request})
            return page.get_paginated_response(comments.data,hand_pick_commnets.data)
        else:
            return page.get_paginated_response(comments.data,'null')


class RevertView(APIView):
    """回复视图"""
    authentication_classes = [Authtication, ]

    def get(self, request):
        """
        获取用户回复
        参数：url参数：comment
        """
        comment_id = request.GET.get('comment')
        reverts_set = Revert.objects.filter(comment=comment_id)

        page = MyRevertPagination()
        page_roles = page.paginate_queryset(queryset=reverts_set, request=request, view=self)
        reverts = RevertInfoSerializer(instance=page_roles, many=True, context={'request': request})

        return page.get_paginated_response(reverts.data)
