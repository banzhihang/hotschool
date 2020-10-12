import random
import time

import redis
from django.contrib.auth.models import AnonymousUser
from rest_framework.response import Response
from rest_framework.views import APIView

from HotSchool.settings import POOL, RECOMMENT_NUMBER
from puclic import get_ordering, LooseAuthtication, check_undefined
from question.models import Answer, Question
from recommend.extra import get_answer_id, mix_answer_and_question, add_user_recommend_record
from recommend.paginations import RecommentQuestionByTimePagination
from recommend.serializers import AnswerRecommendSerializer, QuestionRecommendSerializer, LatestQuestionSerializer


class RecommendView(APIView):
    """推荐视图"""
    authentication_classes = [LooseAuthtication, ]

    @check_undefined
    def get(self, request):
        """获取推荐"""
        school = int(request.GET.get('school', -1))
        type = int(request.GET.get('type', 0))
        coon = redis.Redis(connection_pool=POOL)
        user = request.user

        # 若用户登录
        if not isinstance(user, AnonymousUser):
            user_id = user.pk
            # school为0,则推荐不限学校
            if school == -1:
                # type为0,则为默认推荐,为1则为最新推荐
                if type == 0:
                    # 获得推荐池
                    recommend_list_id = coon.smembers('question:recommend')
                elif type == 1:
                    # 按添加时间排序
                    question_set = Question.objects.all()
            else:
                if type == 0:
                    # 获得推荐池
                    recommend_list_id = coon.smembers('recommend:'+str(school))
                elif type == 1:
                    question_set = Question.objects.filter(school=school)


            if type == 0:
                # 获得用户推荐记录之前,先重新生成用户的推荐记录set,删除分值小于当前时间戳的value
                now_timestamp = time.time()
                coon.zremrangebyscore('recom:' + str(user_id), min=0, max=now_timestamp)
                user_recommend_record_list = set(coon.zrange('recom:' + str(user_id), start=0, end=-1))
                # 去重
                recommend_list = recommend_list_id - user_recommend_record_list
                if recommend_list:
                    # 若推荐池问题数大于RECOMMENT_NUMBER 选择RECOMMENT_NUMBER个问题来推荐,若小于则选择len(recommend_list)个
                    result_id_list = random.sample(
                        recommend_list, RECOMMENT_NUMBER if len(recommend_list)>=RECOMMENT_NUMBER else len(recommend_list))
                    answer_id_list, question_id_list = get_answer_id(result_id_list)
                else:
                    return Response([])

                # 序列化回答
                answer = []
                if answer_id_list:
                    answer_ordering = get_ordering(answer_id_list)
                    answer_set = Answer.objects.filter(id__in=answer_id_list).extra(
                        select={'ordering': answer_ordering},
                        order_by=('ordering',))
                    answer = AnswerRecommendSerializer(instance=answer_set, many=True, context={'request': request})

                # 序列化问题
                question = []
                if question_id_list:
                    question_ordering = get_ordering(question_id_list)
                    question_set = Question.objects.filter(id__in=question_id_list).extra(
                        select={'ordering': question_ordering},
                        order_by=('ordering',))
                    question = QuestionRecommendSerializer(instance=question_set, many=True)

                # 混合回答和问题
                result = mix_answer_and_question(answer.data if answer else [], question.data if question else [])
                # 将推荐过的问题添加到用户推荐记录zset
                add_user_recommend_record(result_id_list, user_id)
                return Response(result)

            else:
                page = RecommentQuestionByTimePagination()
                page_roles = page.paginate_queryset(queryset=question_set, request=request, view=self)
                questions = LatestQuestionSerializer(instance=page_roles, many=True, context={'request': request})

                return page.get_paginated_response(questions.data)
        # 若用户未登录
        else:
            recommend_list_id = coon.srandmember('question:recommend',15)
            answer_id_list, question_id_list = get_answer_id(recommend_list_id)
            # 序列化回答
            answer = []
            if answer_id_list:
                answer_ordering = get_ordering(answer_id_list)
                answer_set = Answer.objects.filter(id__in=answer_id_list).extra(
                    select={'ordering': answer_ordering},
                    order_by=('ordering',))
                answer = AnswerRecommendSerializer(instance=answer_set, many=True, context={'request': request})

            # 序列化问题
            question = []
            if question_id_list:
                question_ordering = get_ordering(question_id_list)
                question_set = Question.objects.filter(id__in=question_id_list).extra(
                    select={'ordering': question_ordering},
                    order_by=('ordering',))
                question = QuestionRecommendSerializer(instance=question_set, many=True)

            # 混合回答和问题
            result = mix_answer_and_question(answer.data if answer else [], question.data if question else [])
            return Response(result)


