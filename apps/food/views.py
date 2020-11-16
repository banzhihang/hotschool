from datetime import datetime,timedelta

from rest_framework.views import APIView

from draft.models import FoodDraft
from puclic import LooseAuthtication, verify_view, check_undefined
from question.tasks import push_to_user
from .paginations import *
from .serializers import *
from .tasks import calculate_food_score


class FoodView(APIView):
    """美食排行视图"""

    @check_undefined
    def get(self, request):
        """
        获取美食排行
        参数:url参数,school_id(学校id),type(若type为0,则为按得分排序,若为1则为按时间排序)
        """
        try:
            school_id = int(request.GET.get('school', 1))
            type = int(request.GET.get('type', 0))
        except:
            return Response('发生错误')

        try:
            food_set = Food.objects.filter(school=school_id).only('id', 'name', 'image_first', 'score')
            # 若type为0,则为按得分排序,若为1则为按时间排序
            if type == 0:
                page = FoodByScorePagination()
                page_roles = page.paginate_queryset(queryset=food_set, request=request, view=self)
                foods = FoodRankSerializer(instance=page_roles, many=True, context={'request': request})

            if type == 1:
                page = FoodByTimePagination()
                page_roles = page.paginate_queryset(queryset=food_set, request=request, view=self)
                foods = FoodRankSerializer(instance=page_roles, many=True, context={'request': request})
        except Exception:
            return Response({'status': 'fail', 'error': '发生错误'})
        else:
            return page.get_paginated_response(foods.data)


class FoodInfoView(APIView):
    """美食详情视图"""
    authentication_classes = [LooseAuthtication, ]

    @check_undefined
    def get(self, request):
        """获取美食详情"""
        try:
            food_id = int(request.GET.get('food'))
        except:
            return Response('发生错误')

        try:
            food_set = Food.objects.get(pk=int(food_id))
            food = FoodInfoSerializer(instance=food_set, many=False, context={'request': request})
            return Response(food.data)
        except Food.DoesNotExist:
            return Response({'error': '未查询到该美食'})

    @verify_view
    def post(self,request):
        """发布美食"""
        ser = PostFoodSerializer(data=request.data,context={'request': request})
        if ser.is_valid():
            food = ser.save()
            FoodDraft.objects.filter(name=food.name,address=food.address).delete()
            return Response({'status':'ok','error':{}})
        else:
            return Response({'status': 'fail', 'error':ser.errors})


class ShortCommentView(APIView):
    """美食短评表"""
    authentication_classes = [LooseAuthtication, ]

    @check_undefined
    def get(self, request):
        """
        获取美食短评
        参数:type(url参数),food(美食id)
        """
        # type为0就是按获赞数排序,为1就是按时间排序
        try:
            type = int(request.GET.get('type', 0))
            food_id = int(request.GET.get('food'))
        except:
            return Response('发生错误')

        try:
            short_comment_set = ShortComment.objects.filter(food=int(food_id))
            if type == 0:
                page = ShortCommentByApprovalNumberPagination()
            else:
                page = ShortCommentByTimePagination()

            page_roles = page.paginate_queryset(queryset=short_comment_set, request=request, view=self)
            short_comment = ShortCommentSerializer(instance=page_roles, many=True, context={'request': request})
            return page.get_paginated_response(short_comment.data)
        except Exception:
            return Response({'error': '发生错误'})


    @verify_view
    def post(self,request):
        """发布短评"""
        ser = PostShortCommentSerializer(data=request.data,context={'request': request})
        if ser.is_valid():
            _,food_id = ser.save()
            coon = redis.Redis(connection_pool=POOL)
            # 判断还未更新分数的set 里面有没有该美食, 有的话直接跳过,没有的话添加定时任务并将该id添加到未更新分数的食物set
            is_exists = coon.sismember('food',food_id)
            if not is_exists:
                coon.sadd('food',food_id)
                execute_time = datetime.fromtimestamp((datetime.now()+timedelta(minutes=10)).timestamp())
                #  十分钟后执行
                calculate_food_score.apply_async(args=[food_id],eta=execute_time)
            return Response({'status': 'ok', 'error': {}})
        else:
            return Response({'status': 'fail', 'error': ser.errors})


class DiscussRankView(APIView):
    """美食讨论视图"""

    @check_undefined
    def get(self, request):
        """
        获取讨论排行
        参数:type(url参数),food(美食id)
        """
        # type为0就是按评论数排序,为1就是按时间排序
        try:
            food_id = int(request.GET.get('food'))
            type = int(request.GET.get('type', 0))
        except:
            return Response('发生错误')

        try:
            discuss_set = Discuss.objects.filter(food=food_id)
            if type == 0:
                page = DiscussByCommentNumberPagination()
            else:
                page = DiscussByTimePagination()

            page_roles = page.paginate_queryset(queryset=discuss_set, request=request, view=self)
            discuss = DiscussRankSerializer(instance=page_roles, many=True, context={'request': request})
            return page.get_paginated_response(discuss.data)
        except Exception:
            return Response({'error': '发生错误'})



class DiscussInfoView(APIView):
    """讨论详情视图"""
    authentication_classes = [LooseAuthtication, ]

    @check_undefined
    def get(self,request):
        """获取讨论详情"""
        try:
            discuss_id = int(request.GET.get('discuss'))
        except:
            return Response('发生错误')

        try:
            discuss_set = Discuss.objects.get(pk=discuss_id)
            discuss = DiscussInfoSerializer(instance=discuss_set,many=False,context={'request': request})
            return Response(discuss.data)
        except Discuss.DoesNotExist:
            return Response({'status': 'fail', 'error': '未查询到该讨论'})


    @verify_view
    def post(self,request):
        """发布讨论"""
        ser = PostDiscussSerializer(data=request.data,context={'request': request})
        if ser.is_valid():
            ser.save()
            return Response({'status': 'ok', 'error': {}})
        else:
            return Response({'status': 'fail', 'error': ser.errors})


    @check_undefined
    @verify_view
    def delete(self,request):
        """
        删除讨论
        参数:discuss(讨论id)
        """
        try:
            discuss_id = int(request.GET.get('discuss'))
        except:
            return Response('发生错误')

        try:
            discuss = Discuss.objects.get(pk=discuss_id)
            # 判断该讨论的评论数是否等于0,若等于零,就可以删除,否则该讨论不可以删除
            if discuss.comment_number == 0:
                # 判断操作发起者是不是作者
                if request.user.pk == discuss.user_id:
                    # 将对应讨论的评论数减一
                    food = Food.objects.get(pk=discuss.food_id)
                    food.discuss_number = F('discuss_number') - 1
                    food.save()
                    discuss.delete()
                    return Response({'status': 'ok', 'error': ''})
                else:
                    return Response({'status': 'fail', 'error':'只有作者可以删除'})
            else:
                return Response({'status': 'fail', 'error': '已经有评论的讨论不能删除'})
        except:
            return Response({'status': 'fail', 'error': '发生错误'})


class FoodCommentView(APIView):
    """美食评论视图"""
    authentication_classes = [LooseAuthtication, ]

    @check_undefined
    def get(self, request):
        """获取评论"""
        try:
            discuss_id = int(request.GET.get('discuss'))
        except:
            return Response('发生错误')

        cursor = request.GET.get('cursor')
        comments_set = FoodComment.objects.filter(discuss=discuss_id)
        page = CommentByTimePagination()
        page_roles = page.paginate_queryset(queryset=comments_set, request=request, view=self)
        comment = DiscussCommentInfoSerializer(instance=page_roles, many=True, context={'request': request})
        # 判断是不是第一次加载,是的话返回数据中就加上精选评论,否则只返回按时间排序的评论
        if not cursor:
            hand_pick_commnets_set = FoodComment.objects.filter(discuss=discuss_id).order_by('-approval_number')[0:5]
            hand_pick_commnets = DiscussCommentInfoSerializer(instance=hand_pick_commnets_set, many=True,
                                                              context={'request': request})
            return page.get_paginated_response(comment.data,hand_pick_commnets.data)
        return page.get_paginated_response(comment.data,[])


    @verify_view
    def post(self,request):
        """发布评论"""
        ser = PostDiscussCommentSerializer(data=request.data,context={'request': request})
        if ser.is_valid():
            comment,target_user_id = ser.save()
            push_to_user.delay(request.user,target_user_id,4,comment)
            return Response({'status': 'ok', 'error': ''})
        else:
            return Response({'status': 'fail', 'error': ser.errors})

    @check_undefined
    @verify_view
    def delete(self,request):
        """删除评论"""
        try:
            comment_id = int(request.GET.get('comment'))
        except:
            return Response('发生错误')

        try:
            comment = FoodComment.objects.get(pk=comment_id)
            # 判断操作发起者是不是作者
            if request.user.pk == comment.user_id:
                # 将对应讨论的评论数减一
                discuss = Discuss.objects.get(pk=comment.discuss_id)
                discuss.comment_number = F('comment_number') - 1
                discuss.save()
                comment.delete()
                return Response({'status': 'ok', 'error': ''})
            else:
                return Response({'status': 'fail', 'error':'只有作者可以删除'})
        except:
            return Response({'status': 'fail', 'error': '发生错误'})



class FoodRevertView(APIView):
    """美食回复视图"""
    authentication_classes = [LooseAuthtication, ]

    @check_undefined
    def get(self,request,):
        """获取美食回复"""
        try:
            comment_id = int(request.GET.get('comment'))
        except:
            return Response('发生错误')

        revert_set = FoodRevert.objects.filter(comment=int(comment_id))
        page = RevertByTimePagination()
        page_roles = page.paginate_queryset(queryset=revert_set, request=request, view=self)
        revert = DiscussRevertInfoSerializer(instance=page_roles, many=True, context={'request': request})

        return page.get_paginated_response(revert.data)

    @verify_view
    def post(self,request):
        """发布回复"""
        ser = PostDiscussRevertSerializer(data=request.data,context={'request': request})
        if ser.is_valid():
            revert,target_user_id = ser.save()
            push_to_user(request.user,target_user_id,5,revert)
            return Response({'status': 'ok', 'error': ''})
        else:
            return Response({'status': 'fail', 'error': ser.errors})

    @check_undefined
    @verify_view
    def delete(self,request):
        """
        删除回复 参数,revert_id
        """
        try:
            revert_id = int(request.GET.get('revert'))
        except:
            return Response('发生错误')

        try:
            revert = FoodRevert.objects.get(pk=revert_id)
            # 判断操作发起者是不是作者
            if request.user.pk == revert.user_id:
                # 将对应评论的回复数减一
                comment = FoodComment.objects.get(pk=revert.comment_id)
                comment.revert_number = F('revert_number') - 1
                comment.save()
                revert.delete()
                return Response({'status': 'ok', 'error': ''})
            else:
                return Response({'status': 'fail', 'error':'只有作者可以删除'})
        except:
            return Response({'status': 'fail', 'error': '发生错误'})
