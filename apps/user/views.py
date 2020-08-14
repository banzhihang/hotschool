from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from puclic import Authtication, get_ordering
from question.serializers import CommentInfoSerializer
from .extra import OpenIdAndImage, modify_headimage_name,uuid_string,create_user_dynamic
from .paginations import UserAttentionPagination, UserCreateByTimePagination, UserCollectPagination, \
    UserDynamicByTimePagination, UserRecentPagination
from .serializers import *


class LoginView(APIView):
    """登录发放token"""

    def post(self, request):
        try:
            jscode = request.data['code']
            nick_name = request.data['nickName']
            head_portrait_url = request.data['avatarUrl']

        except Exception:
            return Response({"msg": "登录失败"})

        # 获得用户openid和头像，若用户存在数据库，则不更新用户昵称和头像(用户可能存在自定义昵称头像)。
        #  若不存在，就用获得的昵称和头像创建用户
        openid, image = OpenIdAndImage(jscode, head_portrait_url).get_openid_image()
        try:
            user = User.objects.get(we_chat_openid=openid)
        except User.DoesNotExist:
            # 使用随机字符串当作用户名，openid当作密码
            user = User.objects.create(nick_name=nick_name, username=uuid_string(),
                                       head_portrait=image, we_chat_openid=openid, password=openid)
            user.save()
        # 拼接头像url
        head_portrait = domain_name+user.head_portrait.url
        # 用户头像
        nick_name = user.nick_name
        # 生成token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return Response({'token': token, "openid": openid,'head_portrait':head_portrait,'nick_name':nick_name})


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
        user = UserInfoSerializer(instance=request.user, context={'request': request})
        return Response(user.data)

    def put(self, request):
        """修改用户信息"""
        # 修改图片名字
        request = modify_headimage_name(request)
        ser = UpdateUserInfoSerializer(data=request.data, instance=request.user)
        if ser.is_valid():
            ser.save()
            return Response({'status': 'ok', 'error': ''})
        else:
            return Response({'status': 'fail', 'error': ser.errors})


class RecentBrowseView(APIView):
    """用户的最近浏览记录"""
    authentication_classes = [Authtication, ]

    def get(self, request):
        """获取用户的浏览记录"""
        # 去redis获得用户浏览的回答的answer.id(已经根据浏览时间排序)组成的列表,并根据该顺序去数据库批量查询，分页后返回前端
        coon = redis.Redis(connection_pool=POOL)
        answer_id = coon.zrevrange('recentbrowse:' + str(request.user.pk), start=0, end=-1)

        # 构造排序条件
        ordering = get_ordering(answer_id)
        # 按该条件的顺序查询得出有序的queryset
        recent_browse_answers = Answer.objects.filter(id__in=answer_id).extra(
            select={'ordering': ordering}, order_by=('ordering',))

        page = UserRecentPagination()
        page_roles = page.paginate_queryset(queryset=recent_browse_answers, request=request, view=self)
        answers = UserRecentBrowseAnswerSerializer(instance=page_roles,
                                                   many=True, context={'request': request})

        return page.get_paginated_response(answers.data)

    def delete(self, request):
        # 删除用户浏览数据，前端传来用户删除的回答的id组成的列表
        # 获得该列表之后去redis将用户数据删除
        answer_record_list = request.data['answer_record_list']
        try:
            coon = redis.Redis(connection_pool=POOL)
            coon.zrem('recentbrowse:' + str(request.user.pk), *answer_record_list)
            status = 'ok'
        except:
            status = 'fail'

        return Response({'status': status})


class MyAnswerView(APIView):
    """用户的回答 评论 回复"""
    authentication_classes = [Authtication, ]

    def get(self, request):
        """
        获取用户的回答评论回复,type=0, 为回答，1为评论，2为回复
        """
        type = int(request.query_params['type'])
        page = UserCreateByTimePagination()
        if type == 0:
            answers = Answer.objects.filter(user=request.user.pk)
            page_roles = page.paginate_queryset(queryset=answers, request=request, view=self)
            answers = UserAnswerInfoSerializer(instance=page_roles, many=True, context={'request': request})
            return page.get_paginated_response(answers.data)
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
        获取用户的收藏,type为0为问题，为1则为回答
        """
        type = int(request.GET.get('type'))
        if type == 0:
            questions = request.user.question_collect.all()
            # 分页
            page = UserCreateByTimePagination()
            page_roles = page.paginate_queryset(queryset=questions, request=request, view=self)
            questions = UserQuestionCollectSerializer(instance=page_roles, many=True)
            return page.get_paginated_response(questions.data)
        else:
            coon = redis.Redis(connection_pool=POOL)
            answers_id_list = coon.smembers('collect:' + str(request.user.pk))
            answers_set = Answer.objects.filter(pk__in=answers_id_list)
            page = UserCollectPagination()
            page_roles = page.paginate_queryset(queryset=answers_set, request=request, view=self)
            answers = UserAnswerCollectSerializer(instance=page_roles, many=True)
            return page.get_paginated_response(answers.data)


class MyAttentionView(APIView):
    """
    用户关注的人
    """
    authentication_classes = [Authtication, ]

    def get(self, request):
        # 获取用户关注的人
        coon = redis.Redis(connection_pool=POOL)
        attention_id_list = coon.smembers('attention:' + str(request.user.pk))
        attention_set = User.objects.filter(pk__in=attention_id_list)
        page = UserAttentionPagination()
        page_roles = page.paginate_queryset(queryset=attention_set, request=request, view=self)
        attentions = UserAttentionSerializer(instance=page_roles, many=True, context={'request': request})
        return page.get_paginated_response(attentions.data)


class UserInfoShowView(APIView):
    """用户详情"""

    def get(self, request, user_id):
        """获取用户创作数据"""
        try:
            userinfo_set = UserData.objects.get(user=user_id)
            userinfo = UserInfoShowSerializer(instance=userinfo_set, many=False, context={'request': request})
        except Exception:
            return Response({'error': '没有该用户'})
        else:
            return Response(userinfo.data)


class UserDynamicView(APIView):
    """用户动态"""

    def get(self, request, user_id):
        """获取用户动态"""
        create_user_dynamic(user_id)
        user_dynamic_set = UserDynamic.objects.filter(user=user_id).select_related('answer')
        if not user_dynamic_set:
            return Response({'next': 'null', 'result': 'null'})
        else:
            page = UserDynamicByTimePagination()
            page_roles = page.paginate_queryset(queryset=user_dynamic_set, request=request, view=self)
            user_dynamic = UserDynamicSerializer(instance=page_roles, many=True)

            return page.get_paginated_response(user_dynamic.data)


class UserAttention(APIView):
    """获取用户的关注信息"""
    def get(self,request,user_id):
        try:
            type = int(request.GET.get('type',0))
        except:
            return Response({'status':'fail','error':'发生错误'})
        # 0表示用户关注的人,1表示关注用户关注的人
        if type in (0,1):
            if type == 0:
                coon = redis.Redis(connection_pool=POOL)
                attention_id_list = coon.smembers('attention:' + str(user_id))
            else:
                coon = redis.Redis(connection_pool=POOL)
                attention_id_list = coon.smembers('beattention:' + str(user_id))
            attention_set = User.objects.filter(pk__in=attention_id_list)

            page = UserAttentionPagination()
            page_roles = page.paginate_queryset(queryset=attention_set, request=request, view=self)
            attentions = UserAttentionSerializer(instance=page_roles, many=True, context={'request': request})
            return page.get_paginated_response(attentions.data)
        else:
            return Response({'status': 'fail', 'error': '发生错误'})


