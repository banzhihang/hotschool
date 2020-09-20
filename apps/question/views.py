from datetime import datetime, timedelta
import time

import redis
from django.contrib.auth.models import AnonymousUser
from django.db.models import F
from rest_framework.response import Response
from rest_framework.views import APIView

from HotSchool.settings import POOL
from draft.models import AnswerDraft
from puclic import get_ordering, LooseAuthtication, Authtication
from .extra import add_question_operation_data, add_user_operation_data
from .models import *
from .paginations import RevertByTimePagination, CommentByTimePagination, AnswerPagination
from .serializers import AnswerInfoSerializer, AnswerBriefSerializer, CommentInfoSerializer, RevertInfoSerializer, \
    HotQuestionSerializer, CreateCommentSerializer, CreateRevertSerializer, QuestionInfoSerializer, \
    PostQuestionSerializer, PostAndUpdateAnswerSerializer
from .tasks import push_to_user, get_answer_abstract_and_first_image


class HotQuestionView(APIView):
    """热门问题视图"""

    def get(self, request):
        """获取热榜问题"""
        school_id = int(request.GET.get('school', 0))
        coon = redis.Redis(connection_pool=POOL)
        today = datetime.now().strftime('%Y%m%d')
        today_hour = datetime.now().hour
        # 以当天日期，例如(20200709)为key去redis查询热榜问题的排名,若查询时间在半夜两点以前,则查询前一天的热榜，大于2则查询今天的热榜
        if today_hour < 2:
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
            hot_question_id_list = coon.zrevrange('hot:' + str(school_id) + ':' + yesterday, start=0, end=14)
        else:
            hot_question_id_list = coon.zrevrange('hot:' + str(school_id) + ':' + today, start=0, end=14)

        # 冷启动情况(小程序上线第一天,问题的热度值还无法统计,所以就先将数据库中的前15条数据当作热榜问题)
        if not hot_question_id_list:
            question_set = Question.objects.filter(school=school_id)[0:14]
            hot_question = HotQuestionSerializer(instance=question_set, many=True, context={'request': request})
            return Response(hot_question.data)

        # 构造排序条件，以redis给出的顺序去数据库查找问题
        ordering = get_ordering(hot_question_id_list)
        hot_question_set = Question.objects.filter(id__in=hot_question_id_list).only('title', 'id').extra(
            select={'ordering': ordering}, order_by=('ordering',))[0:14]

        hot_question = HotQuestionSerializer(instance=hot_question_set, many=True, context={'request': request})

        return Response(hot_question.data)


class QuestionView(APIView):
    """问题视图"""
    authentication_classes = [LooseAuthtication, ]

    def get(self, request):
        """
        获取问题详情
        参数:question_id,type(排序条件)
        """
        question_id = request.GET.get('question')
        answer_type = int(request.GET.get('type', 0))
        page = request.GET.get('page')
        coon = redis.Redis(connection_pool=POOL)
        if not page:
            try:
                question_set = Question.objects.get(pk=question_id)
            except Question.DoesNotExist:
                return Response({'error':'没有该问题'})
            else:
                question = QuestionInfoSerializer(instance=question_set, many=False, context={'request': request})
        #  若type为0,则为默认排序，为1则为按发布时间排序,从redis获取排名
        if int(answer_type) == 0:
            answer_id = coon.zrevrange('answer:score:' + str(question_id), start=0, end=-1)
        else:
            answer_id = coon.zrevrange('answer:time:' + str(question_id), start=0, end=-1)

        if answer_id:
            # 获得排名之后生成去数据库按顺序查询
            ordering = get_ordering(answer_id)
            try:
                answers_set = Answer.objects.filter(question_id=question_id).only('id', 'user', 'modify_time',
                    'abstract','first_image','approval_number', 'comment_number','like_number').extra(
                    select={'ordering': ordering}, order_by=('ordering',))

                pages = AnswerPagination()
                page_roles = pages.paginate_queryset(queryset=answers_set, request=request, view=self)
                answers = AnswerBriefSerializer(instance=page_roles, many=True, context={'request': request})
            except:
                return Response('发生错误')
            else:
                # 将该问题的浏览量加1
                add_question_operation_data('scan', question_id)
                if not page:
                    return pages.get_paginated_response(question.data, answers.data)
                else:
                    return pages.get_paginated_response({}, answers.data)

        # 若没有answei_id说明该问题没有回答
        else:
            # 将该问题的浏览量加1
            add_question_operation_data('scan', question_id)
            return Response({
                'next': None,
                'question': question.data,
                'answer': []
            })

    def post(self, request):
        """发布问题"""
        if isinstance(request.user, AnonymousUser):
            return Response({'error': '未登录'})
        ser = PostQuestionSerializer(data=request.data, context={'request': request})
        if ser.is_valid():
            question = ser.save()
            coon = redis.Redis(connection_pool=POOL)
            # 将该问题id添加到推荐池
            coon.sadd('question:recommend', question.pk)
            coon.sadd('recommend:' + str(question.school_id), question.pk)
            return Response({'status': 'ok', 'error': ''})
        else:
            return Response({'status': 'fail', 'error': ser.errors})


class AnswerView(APIView):
    """回答视图"""
    authentication_classes = [Authtication, ]

    def get(self, request):
        """
        获取回答详情
        参数:answer_id,type(0为默认排序,1为时间排序)
        """
        try:
            answer_id = request.GET.get('answer')
            type = int(request.GET.get('type', 0))
            answer_set = Answer.objects.select_related('question', 'user').get(pk=answer_id)

            answer = AnswerInfoSerializer(instance=answer_set, many=False, context={'request': request})
            # 去redis 获取该回答的排名，并根据该回答的排名获取下一个回答的id, 返回给前端
            coon = redis.Redis(connection_pool=POOL)
        except Exception:
            return Response({'answer': '', 'next': '', 'error': '发生错误'})
        else:
            question, target_user, user = answer_set.question_id, answer_set.user_id, request.user.pk
            #  添加该回答所属问题的浏览量和该问题所属作者的相关数据
            add_question_operation_data('scan', question)
            add_user_operation_data(operation='read', target_user_id=target_user, user_id=user, answer_id=answer_set.id)
            # type为0,为默认排序,为 1则为时间排序
            if int(type) == 0:
                index = coon.zrevrank('answer:score:' + str(question), str(answer_id))
                next_answer_list = coon.zrevrange('answer:score:' + str(question), start=index + 1,
                                                  end=index + 1)
            else:
                index = coon.zrevrank('answer:time:' + str(question), str(answer_id))
                next_answer_list = coon.zrevrange('answer:time:' + str(question), start=index + 1,
                                                  end=index + 1)

            # redis的zrevrange方法返回的是一个列表
            if next_answer_list:
                next_answer = int(next_answer_list[0])
            # 若next_answer_list为None ，则说明为最后一个问题,next_answer就为null
            else:
                next_answer = None

            return Response({'result': answer.data, 'next': next_answer, 'error': ''})

    def delete(self, request):
        """ 删除回答"""
        user_id = request.user.pk
        try:
            answer_id = request.GET.get('answer')
            answer = Answer.objects.select_related('user').get(pk=answer_id)
        except Exception:
            return Response({'msg': 'fail', 'error': '该id不合法'})
        else:
            coon = redis.Redis(connection_pool=POOL)
            # 判断是不是作者本人
            if answer.user.pk == user_id:
                answer.delete()
                # 删除回答的喜欢bzitmap和留存在redis中的数据
                coon.delete('al:' + str(answer_id), 'ad:' + str(answer_id))
                # 将该回答的id从对应问题的回答排行zset删除
                coon.zrem('answer:score:' + str(answer.question_id), answer)
                coon.zrem('answer:time:' + str(answer.question_id), answer)
                question = Question.objects.get(pk=answer.question_id)
                # 将问题的回答数减一
                question.answer_number = F('answer_number') - 1
                question.save()
                return Response({'msg': 'ok', 'error': ''})
            else:
                return Response({'msg': 'fail', 'error': '只有作者可以删除'})

    def post(self, request):
        """发布回答"""
        ser = PostAndUpdateAnswerSerializer(data=request.data, context={'request': request})
        if ser.is_valid():
            answer, question = ser.save()
            # 计算回答的第一张图片url和回答摘要
            get_answer_abstract_and_first_image.delay(answer.pk)
            coon = redis.Redis(connection_pool=POOL)
            now_timestamp = time.time()
            # 将该回答添加到对应问题的redis排行zset
            coon.zadd('answer:score:' + str(question.pk), {answer.pk: float(0)})
            coon.zadd('answer:time:' + str(question.pk), {answer.pk: now_timestamp})
            question.answer_number = F('answer_number') + 1
            question.save()
            # 删除该用户在该回答下的草稿
            AnswerDraft.objects.filter(user_id=request.user.pk,question_id=question.pk).delete()
            # 增加该问题的回答热度数据
            add_question_operation_data('answer', question.pk)
            return Response({'status': 'ok', 'error': ''})
        else:
            return Response({'status': 'fail', 'error': ser.errors})

    def put(self,request):
        """修改回答"""
        answer_id = request.GET.get('answer')
        if answer_id:
            try:
                answer_set = Answer.objects.get(pk=answer_id)
            except Answer.DoesNotExist:
                return Response({'error':'不存在该回答'})
            else:
                # 判断是不是作者本人,不是则直接返回
                if answer_set.pk == request.user.pk:
                    ser = PostAndUpdateAnswerSerializer(instance=answer_set,data=request.data,context={'request': request})
                    if ser.is_valid():
                        ser.save()
                        # 重新计算回答的摘要和第一张图片
                        get_answer_abstract_and_first_image.delay(answer_id)
                        return Response({'status':'ok','error':''})
                    else:
                        return Response({'status': 'ok', 'error': ser.errors})
                else:
                    return Response({'status':'fail','error':'只有作者本人可以修改'})
        else:
            return Response({'status':'fail','error':'发生错误'})


class CommentView(APIView):
    """回答评论视图"""
    authentication_classes = [Authtication, ]

    def get(self, request):
        """
        获取回答或者问题的评论
        参数：answer_id,分页的话，还有cursor
        """
        answer_id = request.GET.get('answer')
        cursor = request.GET.get('cursor')

        if answer_id:
            answer_id = int(answer_id)
            comment_set = Comment.objects.filter(answer=answer_id)

        page = CommentByTimePagination()
        page_roles = page.paginate_queryset(queryset=comment_set, request=request, view=self)
        comments = CommentInfoSerializer(instance=page_roles, many=True, context={'request': request})

        # 若cursor为None,则说明是请求下一页评论,而非第一次加载评论
        if not cursor:
            hand_pick_commnets_set = Comment.objects.filter(answer=answer_id).order_by('-approval_number')
            # 精选评论只有5条
            if hand_pick_commnets_set.count() >= 5:
                hand_pick_commnets_set = hand_pick_commnets_set[0:5]

            hand_pick_commnets = CommentInfoSerializer(instance=hand_pick_commnets_set, many=True,
                                                       context={'request': request})
            return page.get_paginated_response(comments.data, hand_pick_commnets.data)
        else:
            return page.get_paginated_response(comments.data, [])

    def post(self, request):
        """ 发布评论"""
        ser = CreateCommentSerializer(data=request.data, context={'request': request})
        if ser.is_valid():
            comment, target_user, question_id = ser.save()
            push_to_user.delay(request.user, target_user, 1, comment)
            # 添加该评论对应的问题的评论量,回答作者的创作数据增加和回答的评论数增加在序列化器中进行
            add_question_operation_data('comment', question_id)
            return Response({'status': 'ok', 'error': ''})
        else:
            return Response({'status': 'fail', 'error': ser.errors})

    def delete(self, request):
        """删除评论"""
        comment_id = request.GET.get('comment')
        user_id = request.user.pk
        if comment_id:
            comment_id = int(comment_id)
            try:
                commnet = Comment.objects.select_related('user').get(pk=comment_id)
            except Exception:
                return Response({'status': 'fail', 'error': '该id不合法'})
            else:
                # 判断该批评论的作者是不是该用户,只有作者本人能删
                if commnet.user.pk == user_id:
                    commnet.delete()
                    # 将对应回答的评论数减一
                    answer = Answer.objects.get(pk=commnet.answer_id)
                    answer.comment_number = F('comment_number') - 1
                    answer.save()
                    return Response({'status': 'ok', 'error': ''})
                else:
                    return Response({'status': 'fail', 'error': '只有作者可以删除'})
        else:
            return Response({'status': 'fail', 'error': '没有id'})


class RevertView(APIView):
    """回复视图"""
    authentication_classes = [Authtication, ]

    def get(self, request):
        """
        获取回复
        参数：url参数：comment
        """
        comment_id = int(request.GET.get('comment'))
        reverts_set = Revert.objects.filter(comment=comment_id)

        page = RevertByTimePagination()
        page_roles = page.paginate_queryset(queryset=reverts_set, request=request, view=self)
        reverts = RevertInfoSerializer(instance=page_roles, many=True, context={'request': request})

        return page.get_paginated_response(reverts.data)

    def delete(self, request):
        """删除回复"""
        revert_id = request.GET.get('revert')
        user_id = request.user.pk
        if revert_id:
            revert_id = int(revert_id)
            try:
                revert = Revert.objects.select_related('user').get(pk=revert_id)
            except Exception:
                return Response({'status': 'fail', 'error': '该id不合法'})
            else:
                if revert.user.pk == user_id:
                    revert.delete()
                    # 将对应的评论的回复数减一
                    comment = Comment.objects.get(pk=revert.comment_id)
                    comment.revert_number = F('revert_number') - 1
                    comment.save()
                    return Response({'status': 'ok', 'error': ''})
                else:
                    return Response({'status': 'fail', 'error': '只有作者可以删除'})
        else:
            return Response({'status': 'fail', 'error': '没有id'})

    def post(self, request):
        """ 发布回复"""
        # 增加对应评论的回复数放在序列化器中进行
        ser = CreateRevertSerializer(data=request.data, context={'request': request})
        if ser.is_valid():
            revert, target_user_id = ser.save()
            # 异步推送消息给目标用户
            push_to_user.delay(request.user, target_user_id, 3, revert)
            return Response({'status': 'ok', 'error': ''})
        else:
            return Response({'status': 'fail', 'error': ser.errors})


