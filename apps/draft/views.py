from rest_framework.response import Response
from rest_framework.views import APIView

from draft.models import AnswerDraft, FoodDraft
from draft.paginations import AnswerDraftByTimePagination, FoodDraftByTimePagination
from draft.serializers import AnswerDraftInfoSerializer, PostAnswerDraftInfoSerializer, MyAnswerDraftSerializer, \
    MyFoodDraftSerializer, FoodDraftInfoSerializer, PostFoodDraftInfoSerializer
from draft.tasks import get_answer_draft_abstract
from puclic import Authtication, check_undefined


class AnswerDraftView(APIView):
    """回答草稿视图"""
    authentication_classes = [Authtication, ]

    @check_undefined
    def get(self,request):
        """获取草稿详情"""
        try:
            draft_id = int(request.GET.get('draft'))
        except:
            return Response('发生错误')

        try:
            answer_draft_set = AnswerDraft.objects.get(pk=draft_id)
        except AnswerDraft.DoesNotExist:
            return Response('该草稿已删除')
        answer_draft = AnswerDraftInfoSerializer(instance=answer_draft_set,many=False,context={'request': request})
        return Response(answer_draft.data)


    def post(self,request):
        """添加回答草稿"""
        ser = PostAnswerDraftInfoSerializer(data=request.data,context={'request': request})
        if ser.is_valid():
            draft = ser.save()
            # 获得草稿摘要
            get_answer_draft_abstract.delay(draft.pk)
            return Response({'status': 'ok', 'error': ''})
        else:
            return Response({'status': 'fail', 'error': ser.errors})

    def put(self,request):
        """更新草稿"""
        try:
            draft_id = int(request.data.get('draft'))
        except:
            return Response('发生错误')

        try:
            draft = AnswerDraft.objects.get(pk=draft_id)
        except AnswerDraft.DoesNotExist:
            return Response({'status': 'ok', 'error':'未查询到该草稿'})

        ser = PostAnswerDraftInfoSerializer(data=request.data, instance=draft,context={'request': request})
        if ser.is_valid():
            ser.save()
            # 更新草稿摘要
            get_answer_draft_abstract.delay(draft.pk)
            return Response({'status': 'ok', 'error': ''})
        else:
            return Response({'status': 'fail', 'error': ser.errors})

    @check_undefined
    def delete(self,request):
        """删除草稿"""
        try:
            draft_id = int(request.GET.get('draft'))
        except:
            return Response('发生错误')

        user_id = request.user.pk

        try:
            draft = AnswerDraft.objects.get(pk=draft_id)
            if draft.user_id == user_id:
                draft.delete()
            else:
                return Response({'status': 'fail', 'error': '只有作者可以删除'})
        except AnswerDraft.DoesNotExist:
            return Response({'status': 'fail', 'error': '未查询到该草稿'})
        else:
            return Response({'status': 'ok', 'error': ''})


class MyDraftView(APIView):
    """我的草稿视图"""
    authentication_classes = [Authtication, ]

    @check_undefined
    def get(self,request):
        """获取我的草稿"""
        user_id = request.user.pk
        try:
            type = int(request.GET.get('type',0))
        except:
            return  Response('发生错误')

        if type == 0:
            answer_draft_set = AnswerDraft.objects.filter(user=user_id)
            page = AnswerDraftByTimePagination()
            page_roles = page.paginate_queryset(queryset=answer_draft_set, request=request, view=self)
            results = MyAnswerDraftSerializer(instance=page_roles, many=True, context={'request': request})

        elif type == 1:
            food_draft_set = FoodDraft.objects.filter(user=user_id)
            page = FoodDraftByTimePagination()
            page_roles = page.paginate_queryset(queryset=food_draft_set, request=request, view=self)
            results = MyFoodDraftSerializer(instance=page_roles, many=True, context={'request': request})

        else:
            return Response({'status': 'fail', 'error': '没有id'})

        return page.get_paginated_response(results.data)


class FoodDraftView(APIView):
    """美食草稿视图"""
    authentication_classes = [Authtication, ]

    @check_undefined
    def get(self,request):
        """获取草稿详情"""
        try:
            draft_id = int(request.GET.get('draft'))
        except:
            return Response('发生错误')

        try:
            food_draft_set = FoodDraft.objects.get(pk=draft_id)
        except FoodDraft.DoesNotExist:
            return Response('该草稿已删除')
        food_draft = FoodDraftInfoSerializer(instance=food_draft_set, many=False,context={'request': request})
        return Response(food_draft.data)


    def post(self,request):
        """增加草稿"""
        ser = PostFoodDraftInfoSerializer(data=request.data, context={'request': request})
        if ser.is_valid():
            ser.save()
            return Response({'status': 'ok', 'error': ''})
        else:
            return Response({'status': 'fail', 'error': ser.errors})

    def put(self, request):
        """更新草稿"""
        try:
            draft_id = int(request.data.get('draft'))
        except:
            return Response('发生错误')

        try:
            draft = FoodDraft.objects.get(pk=draft_id)
        except FoodDraft.DoesNotExist:
            return Response({'status': 'ok', 'error': '未查询到该草稿'})

        ser = PostFoodDraftInfoSerializer(data=request.data, instance=draft,context={'request': request})
        if ser.is_valid():
            ser.save()
            return Response({'status': 'ok', 'error': ''})
        else:
            return Response({'status': 'fail', 'error': ser.errors})

    @check_undefined
    def delete(self, request):
        """删除草稿"""
        user_id = request.user.pk

        try:
            draft_id = int(request.GET.get('draft'))
        except:
            return Response('发生错误')

        try:
            draft = FoodDraft.objects.get(pk=draft_id)
            if draft.user_id == user_id:
                draft.delete()
            else:
                return Response({'status': 'fail', 'error': '只有作者可以删除'})
        except FoodDraft.DoesNotExist:
            return Response({'status': 'fail', 'error': '未查询到该草稿'})
        else:
            return Response({'status': 'ok', 'error': ''})



