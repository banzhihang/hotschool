from datetime import datetime, timedelta

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from puclic import Authtication, get_ordering, LooseAuthtication, check_undefined
from question.paginations import CollectCommentByTimePagination
from question.serializers import RevertInfoSerializer
from .extra import OpenIdAndImage, uuid_string, create_user_dynamic
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
        openid = OpenIdAndImage(jscode).get_openid()
        if not openid:
            return Response({'msg':'登录失败','status':'fail'})

        try:
            user = User.objects.get(we_chat_openid=openid)
        except User.DoesNotExist:
            # 使用随机字符串当作用户名，openid当作密码
            user = User.objects.create(nick_name=nick_name, username=uuid_string(),
                                       head_portrait=head_portrait_url, we_chat_openid=openid, password=openid)
            # 同时创建用户的创作者数据表
            UserData.objects.create(user_id=user.pk)

        head_portrait, nick_name, user_id, school = user.head_portrait, user.nick_name, user.pk, user.school.id
        # 生成token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return Response({'id': user_id, 'token': token, "openid": openid, 'head_portrait': head_portrait,
                         'nick_name': nick_name,'school': school,'status':'ok'})


class UserInfoView(APIView):
    """用户信息"""
    authentication_classes = [Authtication, ]

    @check_undefined
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
        ser = UpdateUserInfoSerializer(data=request.data, instance=request.user)
        if ser.is_valid():
            ser.save()
            return Response({'status': 'ok', 'error': ''})
        else:
            return Response({'status': 'fail', 'error': ser.errors})


class RecentBrowseView(APIView):
    """用户的最近浏览记录"""
    authentication_classes = [Authtication, ]

    @check_undefined
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
        answers = UserRecentBrowseAnswerSerializer(instance=page_roles, many=True, context={'request': request})

        return page.get_paginated_response(answers.data)

    def delete(self, request):
        # 删除用户浏览数据，前端传来用户删除的回答的id组成的列表
        # 获得该列表之后去redis将用户数据删除
        answer_record_list = request.data.get("answer_record_list")
        if answer_record_list:
            try:
                coon = redis.Redis(connection_pool=POOL)
                coon.zrem('recentbrowse:' + str(request.user.pk), *answer_record_list)
                status = 'ok'
            except:
                status = 'fail'
            return Response({'status': status})
        else:
            return Response("错误")


class MyPublishView(APIView):
    """用户的问题,回答,评论,美食"""
    authentication_classes = [Authtication, ]

    @check_undefined
    def get(self, request):
        """
        获取用户的回答问题美食,type=0为回答，1为问题,2为评论,3为美食
        """
        try:
            type = int(request.GET.get('type'))
        except:
            return Response('发生错误')

        page = UserCreateByTimePagination()
        if type == 0:
            answers = Answer.objects.filter(user=request.user.pk)
            page_roles = page.paginate_queryset(queryset=answers, request=request, view=self)
            answers = UserAnswerInfoSerializer(instance=page_roles, many=True, context={'request': request})
            return page.get_paginated_response(answers.data)

        elif type == 1:
            question_set = Question.objects.filter(user=request.user.pk)
            page_roles = page.paginate_queryset(queryset=question_set, request=request, view=self)
            questions = UserQuestionPublishSerializer(instance=page_roles, many=True, context={'request': request})
            return page.get_paginated_response(questions.data)

        elif type == 2:
            comment_set = Comment.objects.filter(user=request.user.pk)
            page_roles = page.paginate_queryset(queryset=comment_set, request=request, view=self)
            comments = UserCommentInfoSerializer(instance=page_roles, many=True, context={'request': request})
            return page.get_paginated_response(comments.data)

        elif type == 3:
            foods_set = Food.objects.filter(user=request.user.pk)
            page_roles = page.paginate_queryset(queryset=foods_set, request=request, view=self)
            foods = UserFoodInfoSerializer(instance=page_roles, many=True, context={'request': request})
            return page.get_paginated_response(foods.data)

        else:
            return Response({'error': '发生错误'})


class MyCollectView(APIView):
    """用户的收藏"""
    authentication_classes = [Authtication, ]

    @check_undefined
    def get(self, request):
        """
        获取用户的收藏,type为0为问题，为1则为回答,2为美食
        """
        try:
            type = int(request.GET.get('type'))
        except:
            return Response('发生错误')
        else:
            if type == 0:
                questions = UserCollectQuestion.objects.select_related('question').filter(user_id=request.user.pk)
                # 分页
                page = UserCreateByTimePagination()
                page_roles = page.paginate_queryset(queryset=questions, request=request, view=self)
                questions = UserQuestionCollectSerializer(instance=page_roles, many=True)
                return page.get_paginated_response(questions.data)

            elif type == 1:
                coon = redis.Redis(connection_pool=POOL)
                answers_id_list = coon.smembers('collect:' + str(request.user.pk))
                answers_set = Answer.objects.filter(pk__in=answers_id_list)
                page = UserCollectPagination()
                page_roles = page.paginate_queryset(queryset=answers_set, request=request, view=self)
                answers = UserAnswerCollectSerializer(instance=page_roles, many=True)
                return page.get_paginated_response(answers.data)

            elif type == 2:
                user = request.user
                foods_set = UserCollectFood.objects.filter(user=user.pk)
                page = UserCreateByTimePagination()
                page_roles = page.paginate_queryset(queryset=foods_set, request=request, view=self)
                foods = UserFoodCollectSerializer(instance=page_roles, many=True)
                return page.get_paginated_response(foods.data)
            else:
                return Response({'error': '发生错误'})


class UserInfoShowView(APIView):
    """用户详情(用户信息展示)"""
    authentication_classes = [LooseAuthtication, ]

    @check_undefined
    def get(self, request, user_id):
        """获取用户创作数据"""
        try:
            user_id = int(user_id)
        except:
            return Response('发生错误')

        try:
            userinfo_set = UserData.objects.get(user=user_id)
        except UserData.DoesNotExist:
            return Response({'error': '没有该用户'})
        else:
            userinfo = UserInfoShowSerializer(instance=userinfo_set, many=False, context={'request': request})
            return Response(userinfo.data)


class UserDynamicView(APIView):
    """用户动态"""

    @check_undefined
    def get(self, request, user_id):
        """获取用户动态"""

        # 获取用户动态前先将redis中的动态同步到数据库
        create_user_dynamic(user_id)
        user_dynamic_set = UserDynamic.objects.filter(user=user_id).select_related('answer')
        if not user_dynamic_set:
            return Response({'next': None, 'result': None})
        else:
            page = UserDynamicByTimePagination()
            page_roles = page.paginate_queryset(queryset=user_dynamic_set, request=request, view=self)
            user_dynamic = UserDynamicSerializer(instance=page_roles, many=True)

            return page.get_paginated_response(user_dynamic.data)


class UserAttention(APIView):
    """获取用户的关注信息"""
    authentication_classes = [LooseAuthtication, ]

    @check_undefined
    def get(self, request, user_id):
        try:
            type = int(request.GET.get('type', 0))
        except:
            return Response('发生错误')
        # 0表示用户关注的人,1表示关注用户关注的人
        if type in (0, 1):
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


class UserCreatorDataView(APIView):
    """用户昨天的创作者数据"""
    authentication_classes = [Authtication, ]

    @check_undefined
    def get(self, request):
        """获得用户昨日的创作者数据"""
        user_id = request.user.pk
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')  # 昨天的时间字符串
        coon = redis.Redis(connection_pool=POOL)
        is_exist = coon.exists('ud:' + yesterday + ':' + str(user_id))
        if is_exist:
            user_data = coon.hmget('ud:' + yesterday + ':' + str(user_id), 'read', 'approval', 'like', 'collect',
                                   'attention')
            data = {
                'read': int(user_data[0]),
                'approval': int(user_data[1]),
                'like': int(user_data[2]),
                'collect': int(user_data[3]),
                'attention': int(user_data[4])
            }
            return Response(data)
        else:
            data = {
                'read': 0,
                'approval': 0,
                'like': 0,
                'collect': 0,
                'attention': 0
            }
            return Response(data)


class CollectCommentInfoView(APIView):
    """我的发布中评论详情"""
    authentication_classes = [Authtication, ]

    @check_undefined
    def get(self, request):
        """获得评论详情"""
        cursor = int(request.GET.get('cursor'))
        try:
            comment_id = int(request.GET.get('comment'))
        except:
            return Response('发生错误')

        try:
            comment_set = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Response({"error": '没有该评论'})
        else:
            revert_set = Revert.objects.filter(comment_id=comment_id)
            page = CollectCommentByTimePagination()
            page_roles = page.paginate_queryset(queryset=revert_set, request=request, view=self)
            reverts = RevertInfoSerializer(instance=page_roles, many=True, context={'request': request})
            # 若不存在cursor,则说明请求的是第一页,返回评论数据,若存在cursor,则说明不是第一页,返回的数据中commnet为{}
            if not cursor:
                comment = CollectCommentInfoSerializer(instance=comment_set, many=False,
                                                       context={'request': request})
                return page.get_paginated_response(comment.data, reverts.data)
            else:
                return page.get_paginated_response({}, reverts.data)



class HelloWorldView(APIView):
    """测试视图"""
    def get(self,request):
        return Response("hello! Is Ok!")