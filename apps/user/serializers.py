import time

import redis
from rest_framework import serializers

from HotSchool.settings import POOL, ANONYMITY_USER_HEAD_IMAGE
from food.models import Food
from puclic import verify_serializers
from question.models import *
from upload.extra import QiNiuFileManage
from user.models import *


class UserInfoSerializer(serializers.ModelSerializer):
    """用户数据序列化器"""
    nick_name = serializers.CharField()
    desc = serializers.CharField(default='')
    school = serializers.CharField(source='school.name',default='')

    class Meta:
        model = User
        fields = ['nick_name', 'head_portrait','desc', 'school']


class UpdateUserInfoSerializer(serializers.ModelSerializer):
    """
    修改用户信息序列化器
    必须字段:无,选要字段:nick_namedesc,school
    """
    nick_name = serializers.CharField(min_length=1, max_length=10, required=False, error_messages={
        'min_length': '昵称最低1个字符',
        'max_length': '昵称最大10字符'
    })
    desc = serializers.CharField(min_length=5, max_length=30, required=False, error_messages={
        'min_length': '个人描述最低5个字符',
        'max_length': '个人描述最大30字符'})


    def update(self, instance, validated_data):
        # 更新头像之前先删除存储在七牛云上的旧图片
        old_picture_url = instance.head_portrait
        _,_ = QiNiuFileManage(old_picture_url).delete()
        return User.objects.filter(id=instance.id).update(**validated_data)

    class Meta:
        model = User
        fields = ['nick_name','head_portrait','desc','school']


class UserRecentBrowseAnswerSerializer(serializers.ModelSerializer):
    """最近浏览回答序列化器"""
    user_nick_name = serializers.CharField(source='user.nick_name')
    question_title = serializers.CharField(source='question.title')

    class Meta:
        model = Answer
        fields = ['id', 'user_nick_name', 'approval_number','comment_number','abstract','question_title']


class UserAttentionSerializer(serializers.ModelSerializer):
    """用户关注序列化器"""
    is_attention = serializers.SerializerMethodField()

    @verify_serializers(type=0)
    def get_is_attention(self,obj,user):
        coon = redis.Redis(connection_pool=POOL)
        is_attention = coon.sismember('attention:' + str(user.pk), obj.pk)
        if is_attention:
            return 1
        else:
            return 0

    class Meta:
        model = User
        fields = ['id','nick_name','head_portrait','desc','is_attention']


class UserQuestionCollectSerializer(serializers.ModelSerializer):
    """用户收藏的问题序列化器"""
    id = serializers.IntegerField(source='question.id')
    title = serializers.CharField(source='question.title')
    answer_number = serializers.IntegerField(source='question.answer_number')
    attention_number = serializers.IntegerField(source='question.attention_number')

    class Meta:
        model = UserCollectQuestion
        fields = ['id', 'title','answer_number','attention_number']


class UserQuestionPublishSerializer(serializers.ModelSerializer):
    """用户发布的问题序列化器"""

    class Meta:
        model = Question
        fields = ['id', 'title','answer_number','attention_number']


class UserAnswerCollectSerializer(serializers.ModelSerializer):
    """用户收藏的回答序列化器"""
    user_head_portrait = serializers.SerializerMethodField()
    user_nick_name = serializers.SerializerMethodField()
    question_title = serializers.CharField(source='question.title')

    def get_user_head_portrait(self,answer):
        if answer.is_anonymity == 1:
            return ANONYMITY_USER_HEAD_IMAGE
        else:
            return answer.user.head_portrait

    def get_user_nick_name(self, answer):
        if answer.is_anonymity == 1:
            return '匿名用户'
        else:
            return answer.user.nick_name

    class Meta:
        model = Answer
        fields = ['id','question_title','user_head_portrait',
                  'user_nick_name','abstract','approval_number','comment_number']


class UserRevertInfoSerializer(serializers.ModelSerializer):
    """用户的回复信息序列化"""
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    user = serializers.IntegerField(source='user.pk')
    comment_content = serializers.CharField(source='comment.content')
    question_title = serializers.CharField(source='comment.question.title')
    user_nick_name = serializers.CharField(source='user.nick_name')
    user_head_portrait = serializers.URLField(source='user.head_portrait')
    target_user_nick_name = serializers.CharField(source='target_user.nick_name')
    target_user = serializers.IntegerField(source='target_user.pk')

    class Meta:
        model = Revert
        fields = ['id','user','user_nick_name','target_user',
                  'target_user_nick_name','user_head_portrait','comment_content',
                  'question_title','content','approval_number','add_time']


class UserCommentInfoSerializer(serializers.ModelSerializer):
    """用户评论序列化器"""
    question = serializers.IntegerField(source='answer.question.pk')
    question_title = serializers.CharField(source='answer.question.title')
    answer = serializers.IntegerField(source='answer.pk')

    class Meta:
        model = Comment
        fields = ['id','question','question_title','answer','content','approval_number','revert_number']


class UserFoodInfoSerializer(serializers.ModelSerializer):
    """用户的美食信息序列化器"""
    score = serializers.SerializerMethodField()
    desc = serializers.SerializerMethodField()

    def get_score(self,obj):
        """将分数值舍入到小数点一位来显示"""
        if obj.vote_number <10:
            return None
        else:
            return round(obj.score,1)

    def get_desc(self,obj):
        """获得描述,字数大于13就截断同时添加..."""
        desc = obj.desc
        if len(desc)<13:
            return desc
        else:
            return desc[0:13]+'...'

    class Meta:
        model = Food
        fields = ['id','name','image_first','score','desc']


class UserFoodCollectSerializer(serializers.ModelSerializer):
    """用户美食收藏序列化器"""
    id = serializers.IntegerField(source='food.id')
    name = serializers.CharField(source='food.name')
    desc = serializers.SerializerMethodField()
    image_first = serializers.CharField(source='food.image_first')
    score = serializers.SerializerMethodField()

    def get_score(self,obj):
        """将分数值舍入到小数点一位来显示"""
        if obj.food.vote_number <10:
            return None
        else:
            return round(obj.food.score,1)

    def get_desc(self,obj):
        """获得描述,字数大于13就截断同时添加..."""
        desc = obj.food.desc
        if len(desc)<13:
            return desc
        else:
            return desc[0:13]+'...'

    class Meta:
        model = UserCollectFood
        fields = ['id','name','image_first','score','desc']


class UserAnswerInfoSerializer(serializers.ModelSerializer):
    """用户回答信息序列化"""
    user_nick_name = serializers.CharField(source='user.nick_name')
    question_title = serializers.CharField(source='question.title')
    user_head_portrait = serializers.URLField(source='user.head_portrait')


    class Meta:
        model = Answer
        fields = ['id','user_nick_name','approval_number','comment_number','abstract','user_head_portrait','question_title']


class UserInfoShowSerializer(serializers.ModelSerializer):
    """用户信息展示序列化器"""
    nick_name = serializers.CharField(source='user.nick_name')
    desc = serializers.CharField(source='user.desc',default='')
    head_portrait = serializers.URLField(source='user.head_portrait')
    school_name = serializers.CharField(source='user.school.name')
    collect_user_number = serializers.SerializerMethodField()
    user_be_collect_number = serializers.SerializerMethodField()
    is_attention = serializers.SerializerMethodField()

    def get_collect_user_number(self,obj):
        # 从redis获取关注用户的人的数量
        coon = redis.Redis(connection_pool=POOL)
        # scard方法 若没有检测到该键，则返回0
        number = coon.scard('beattention:'+str(obj.user_id))
        return number

    def get_user_be_collect_number(self,obj):
        # 从redis获取用户关注的人的数量
        coon = redis.Redis(connection_pool=POOL)
        number = coon.scard('attention:' + str(obj.user_id))
        return number

    @verify_serializers(type=0)
    def get_is_attention(self,obj,user):
        coon = redis.Redis(connection_pool=POOL)
        is_attention = coon.sismember('attention:'+str(user.pk),obj.pk)
        if is_attention:
            return 1
        else:
            return 0

    class Meta:
        model = UserData
        fields = ['user','nick_name','desc','school_name','head_portrait','collect_user_number','user_be_collect_number',
                  'approval_number','like_number','collect_number','read_number','is_attention']


class UserDynamicSerializer(serializers.ModelSerializer):
    """用户动态序列化器"""
    type = serializers.IntegerField()
    add_time = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    user_head_portrait = serializers.URLField(source='user.head_portrait')
    user_nick_name = serializers.CharField(source='user.nick_name')

    def get_content(self,obj):
        # 若type在1，2，3里面，则序列化回答，否则序列化问题
        if obj.type in [0,1,2]:
            content = UserDynamicAnswerSerializer(instance=obj.answer)
        else:
            content = UserQuestionPublishSerializer(instance=obj.question)
        return content.data

    def get_add_time(self,obj):
        time_array = time.localtime(obj.add_time)
        return time.strftime('%Y-%m-%d %H:%M',time_array)

    class Meta:
        model = UserDynamic
        fields = ['type','add_time','user_head_portrait','content','user_nick_name']


class UserDynamicAnswerSerializer(serializers.ModelSerializer):
    """用户动态回答序列化器"""
    question_title = serializers.CharField(source='question.title')
    user_nick_name = serializers.CharField(source='user.nick_name')

    class Meta:
        model = Answer
        fields = ['id','question_title','user_nick_name','approval_number','comment_number','abstract','first_image']


class CollectCommentInfoSerializer(serializers.ModelSerializer):
    """我的发布中评论详情序列化器"""
    nick_name = serializers.CharField(source='user.nick_name')
    head_portrait = serializers.URLField(source='user.head_portrait')
    question = serializers.IntegerField(source='answer.question.pk')
    question_title = serializers.CharField(source='answer.question.title')
    answer = serializers.IntegerField(source='answer.pk')
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = Comment
        fields = ['id','question','nick_name','head_portrait','question_title','answer','add_time','content',
                  'revert_number']






