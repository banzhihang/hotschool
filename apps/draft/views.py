from rest_framework.response import Response
from rest_framework.views import APIView

from draft.models import AnswerDraft, FoodDraft
from draft.paginations import AnswerDraftByTimePagination, FoodDraftByTimePagination
from draft.serializers import AnswerDraftInfoSerializer, PostAnswerDraftInfoSerializer, MyAnswerDraftSerializer, \
    MyFoodDraftSerializer, FoodDraftInfoSerializer, PostFoodDraftInfoSerializer
from puclic import Authtication, check_undefined


class AnswerDraftView(APIView):
    """回答草稿视图"""
    authentication_classes = [Authtication, ]

    @check_undefined
    def get(self,request):
        """获取草稿详情"""
        draft_id = request.GET.get('draft')
        if draft_id:
            try:
                answer_draft_set = AnswerDraft.objects.get(pk=draft_id)
            except:
                return Response('该草稿已删除')
            answer_draft = AnswerDraftInfoSerializer(instance=answer_draft_set,many=False,context={'request': request})
            return Response(answer_draft.data)
        else:
            return Response('发生错误')

    def post(self,request):
        """添加回答草稿"""
        ser = PostAnswerDraftInfoSerializer(data=request.data,context={'request': request})
        if ser.is_valid():
            ser.save()
            return Response({'status': 'ok', 'error': ''})
        else:
            return Response({'status': 'fail', 'error': ser.errors})

    def put(self,request):
        """更新草稿"""
        draft_id = request.data.get('draft')
        if draft_id:
            draft = AnswerDraft.objects.get(pk=request.data['draft'])
        else:
            return Response({'status': 'ok', 'error':'无id'})
        ser = PostAnswerDraftInfoSerializer(data=request.data, instance=draft,context={'request': request})
        if ser.is_valid():
            ser.save()
            return Response({'status': 'ok', 'error': ''})
        else:
            return Response({'status': 'fail', 'error': ser.errors})

    @check_undefined
    def delete(self,request):
        """删除草稿"""
        answer_draft_id = request.GET.get('draft')
        user_id = request.user.pk
        if answer_draft_id:
            try:
                draft = AnswerDraft.objects.get(pk=answer_draft_id)
                if draft.user_id == user_id:
                    draft.delete()
                else:
                    return Response({'status': 'fail', 'error': '只有作者可以删除'})
            except:
                return Response({'status': 'fail', 'error': '发生错误'})
            else:
                return Response({'status': 'ok', 'error': ''})
        else:
            return Response({'status': 'fail', 'error': '没有id'})


class MyDraftView(APIView):
    """我的草稿视图"""
    authentication_classes = [Authtication, ]

    @check_undefined
    def get(self,request):
        """获取我的草稿"""
        user_id = request.user.pk
        type = request.GET.get('type',0)
        try:
            type = int(type)
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
        draft_id = request.GET.get('draft')
        if draft_id:
            try:
                food_draft_set = FoodDraft.objects.get(pk=draft_id)
            except:
                return Response('该草稿已删除')
            food_draft = FoodDraftInfoSerializer(instance=food_draft_set, many=False,context={'request': request})
            return Response(food_draft.data)
        else:
            return Response('发生错误')

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
        draft_id = request.data.get('draft')
        if draft_id:
            draft = FoodDraft.objects.get(pk=draft_id)
        else:
            return Response({'status': 'ok', 'error': '无id'})
        ser = PostFoodDraftInfoSerializer(data=request.data, instance=draft,context={'request': request})
        if ser.is_valid():
            ser.save()
            return Response({'status': 'ok', 'error': ''})
        else:
            return Response({'status': 'fail', 'error': ser.errors})

    @check_undefined
    def delete(self, request):
        """删除草稿"""
        food_draft_id = request.GET.get('draft')
        user_id = request.user.pk
        if food_draft_id:
            try:
                draft = FoodDraft.objects.get(pk=food_draft_id)
                if draft.user_id == user_id:
                    draft.delete()
                else:
                    return Response({'status': 'fail', 'error': '只有作者可以删除'})
            except:
                return Response({'status': 'fail', 'error': '发生错误'})
            else:
                return Response({'status': 'ok', 'error': ''})
        else:
            return Response({'status': 'fail', 'error': '没有id'})


