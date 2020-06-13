
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from question.serializers import AnswerInfoSerializer, QuestionInfoSerializer, CommentInfoSerializer, \
    RevertInfoSerializer
from .extra import OpenIdAndImage, modify_image_name,Authtication,random_string
from .logics import *
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
            return Response({'state': 'ok'})
        else:
            return Response({'error':ser.errors})


class RecentBrowseView(APIView):
    """用户的最近浏览记录"""
    authentication_classes = [Authtication, ]

    def get(self, request):
        """获取用户的浏览记录"""
        recent_browse_questions = RecentBrowseQuestion.objects.filter(
            user=request.user.pk)
        recent_browse_answers = RecentBrowseAnswer.objects.filter(
            user=request.user.pk)

        questions = UserRecentBrowseQuestionSerializer(instance=recent_browse_questions,
                                                       many=True,context={'request':request})
        answers = UserRecentBrowseAnswerSerializer(instance=recent_browse_answers,
                                                   many=True,context={'request':request})

        return Response({'questions': questions.data, 'answers': answers.data})

    def delete(self,request):
        # 删除用户浏览数据，前端传来用户删除的问题和回答id的列表(两个列表)
        # 获得该列表之后去RecentBrowseAnswer，RecentBrowseAnswer这两个表将用户数据删除
        answter_record_list = request.data['answter_record_list']
        question_record_list = request.data['question_record_list']

        state1,state2 = delete_recent_browse(request,answter_record_list,question_record_list)

        return Response({'Astate':state1,'Qstate':state2})


class MyAnswerView(APIView):
    """用户的回答 评论 回复"""
    authentication_classes = [Authtication, ]

    def get(self, request):
        """获取用户的回答评论回复"""
        answers = Answer.objects.filter(user=request.user.pk)
        comments = Comment.objects.filter(user=request.user.pk)
        reverts = Revert.objects.filter(user=request.user.pk)

        answers = AnswerInfoSerializer(instance=answers, many=True,context={'request':request})
        comments = CommentInfoSerializer(instance=comments,many=True,context={'request':request})
        reverts = UserRevertInfoSerializer(instance=reverts,many=True,context={'request':request})

        return Response({'answers':answers.data,'comments':comments.data,'reverts':reverts.data})


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
        """获取用户的收藏"""
        questions = request.user.question_collect.all()
        answers = request.user.answer_collect.all()

        questions = UserQuestionCollectSerializer(instance=questions, many=True)
        answers = AnswerInfoSerializer(instance=answers, many=True,context={'request':request})

        return Response({'questions': questions.data, 'answers': answers.data})


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
            return Response({'state':'fail'})
        else:
            return Response({'state': 'success'})


