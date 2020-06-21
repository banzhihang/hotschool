from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from question.serializers import CommentInfoSerializer
from .extra import OpenIdAndImage, modify_image_name,Authtication,random_string,MyCursorPagination
from .serializers import *


class LoginView(APIView):
    """登录发放token"""

    def post(self, request):
        try:
            jscode = request.data['code']
            nick_name = request.data['nickName']
            head_portrait_url = request.data['avatarUrl']

        except Exception as e:
            return Response({"msg": "登录失败"})

        # 获得用户openid和头像，若用户存在数据库，则不更新用户昵称和头像(用户可能存在自定义昵称头像)。
        #  若不存在，就用获得的昵称和头像创建用户
        openid, image = OpenIdAndImage(jscode,head_portrait_url).get_openid_image()
        try:
            user = User.objects.get(we_chat_openid=openid)
        except User.DoesNotExist:
            # 使用随机字符串当作用户名，openid当作密码
            user = User.objects.create(nick_name=nick_name, username=random_string(),
                                     head_portrait=image,we_chat_openid=openid,password=openid)
            user.save()

        # 生成token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return Response({'token': token, "openid": openid})


class UserInfoView(APIView):
    """用户信息"""

    authentication_classes = [Authtication, ]

    def get(self, request):
        """
        获取用户信息
         参数:无
         要求:必须带上token
         返回值:包含用户信息的一个字典
        """
        user = UserInfoSerializer(instance=request.user,context={'request': request})
        return Response(user.data)

    def put(self,request):
        """修改用户信息"""
        user = User.objects.get(pk=request.user.pk)
        # 修改图片名字
        request = modify_image_name(request)
        ser = UpdateUserInfoSerializer(data=request.data,instance=user)
        if ser.is_valid():
            ser.save()
            return Response({'status':'ok','error':''})
        else:
            return Response({'status':'fail','error':ser.errors})


class RecentBrowseView(APIView):
    """用户的最近浏览记录"""
    authentication_classes = [Authtication, ]

    def get(self, request):
        """获取用户的浏览记录"""
        recent_browse_answers = RecentBrowseAnswer.objects.filter(
            user=request.user.pk)

        page = MyCursorPagination()
        page_roles = page.paginate_queryset(queryset=recent_browse_answers, request=request, view=self)
        answers = UserRecentBrowseAnswerSerializer(instance=page_roles,
                                    many=True,context={'request':request})

        return page.get_paginated_response(answers.data)

    def delete(self,request):
        # 删除用户浏览数据，前端传来用户删除的回答的id组成的列表
        # 获得该列表之后去RecentBrowseAnswer表将用户数据删除
        answter_record_list = request.data['answter_record_list']
        try:
            RecentBrowseAnswer.objects.filter(answer_id__in=answter_record_list,
                                          user_id=request.user.id).delete()
            status = 'ok'
        except:
            status = 'fail'

        return Response({'Astatus':status})


class MyAnswerView(APIView):
    """用户的回答 评论 回复"""
    authentication_classes = [Authtication, ]

    def get(self, request):
        """
        获取用户的回答评论回复,type=0, 为回答，1为评论，2为回复
        """
        type = int(request.query_params['type'])
        page = MyCursorPagination()
        if type == 0:
            answers = Answer.objects.filter(user=request.user.pk)
            page_roles = page.paginate_queryset(queryset=answers, request=request, view=self)
            answers = UserAnswerInfoSerializer(instance=page_roles, many=True, context={'request': request})
            return  page.get_paginated_response(answers.data)
        elif type == 1:
            comments = Comment.objects.filter(user=request.user.pk)
            page_roles = page.paginate_queryset(queryset=comments, request=request, view=self)
            comments = CommentInfoSerializer(instance=page_roles, many=True, context={'request': request})
            return page.get_paginated_response(comments.data)
        elif type == 2:
            reverts = Revert.objects.filter(user=request.user.pk)
            page_roles = page.paginate_queryset(queryset=reverts, request=request, view=self)
            reverts = UserRevertInfoSerializer(instance=page_roles, many=True, context={'request': request})
            return page.get_paginated_response(reverts.data)


class MyQuestionView(APIView):
    """用户的问题"""
    authentication_classes = [Authtication, ]

    def get(self, request):
        """获取用户的问题"""
        # 获得问题的queryset
        question = Question.objects.filter(user=request.user.pk)
        # 序列化
        questions = UserQuestionCollectSerializer(instance=question, many=True)

        return Response(questions.data)


class MyCollectView(APIView):
    """用户的收藏"""
    authentication_classes = [Authtication, ]

    def get(self, request):
        """
        获取用户的收藏,type为0，为问题，为1则为回答
        """
        type = int(request.query_params['type'])
        if type == 0:
            questions = request.user.question_collect.all()
            # 分页
            page = MyCursorPagination()
            page_roles = page.paginate_queryset(queryset=questions, request=request, view=self)
            questions = UserQuestionCollectSerializer(instance=page_roles, many=True)
            return page.get_paginated_response(questions.data)
        else:
            answers = request.user.answer_collect.all()
            page = MyCursorPagination()
            page_roles = page.paginate_queryset(queryset=answers, request=request, view=self)
            answers = UserAnswerCollectSerializer(instance=page_roles, many=True)
            return page.get_paginated_response(answers.data)


class MyAttentionView(APIView):
    """
    用户关注的人
    """
    authentication_classes = [Authtication, ]

    def get(self, request):
        # 获取用户关注的人
        attention = request.user.attention.all()
        attentions = UserAttentionSerializer(instance=attention,many=True,
                                             context={'request': request})
        return Response(attentions.data)

    def delete(self,request):
        """取消用户关注的人"""
        target_user_id = request.data['target_id']
        try:
            # 同时删除两张表中的记录，保持数据一致
            request.user.attention.remove(target_user_id)
            AttentionRelation.objects.get(target_user=target_user_id,user=request.user.pk).delete()
        except:
            return Response({'status':'fail'})
        else:
            return Response({'status': 'success'})


