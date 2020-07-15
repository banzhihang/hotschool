import redis
from rest_framework import serializers

from HotSchool.settings import domain_name
from user.extra import POOL
from .models import *


class QuestionInfoSerializer(serializers.ModelSerializer):
    """问题信息序列化"""
    add_time = serializers.DateField(format='%Y-%m-%d')
    modify_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    interest_circle = serializers.SerializerMethodField()

    def get_interest_circle(self,obj):
        interests = obj.interest_circle.all()
        interests = [interest.name for interest in interests]

        return interests

    class Meta:
        model = Question
        fields = "__all__"


class AnswerInfoSerializer(serializers.ModelSerializer):
    """回答信息序列化"""
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    modify_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    user_head_portrait = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    user_nick_name = serializers.SerializerMethodField()
    user_desc = serializers.SerializerMethodField()
    is_approval = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    is_collect = serializers.SerializerMethodField()
    is_attention_user = serializers.SerializerMethodField()

    def get_user_head_portrait(self,answer):
        if answer.is_anonymity == 1:
            path = domain_name + '/media/headimage/anonymity.jpg'
            return path
        else:
            return domain_name + answer.user.head_portrait.url

    def get_user_nick_name(self, answer):
        if answer.is_anonymity == 1:
            return '匿名用户'
        else:
            return answer.user.nick_name

    def get_user(self,answer):
        if answer.is_anonymity == 1:
            return 'null'
        else:
            return answer.user_id

    def get_user_desc(self,answer):
        if answer.is_anonymity == 1:
            return 'null'
        else:
            return answer.user.desc

    def get_is_approval(self,answer):
        # 判断用户对该问题的赞同情况,1为喜欢,0为不喜欢,2为未表态
        user_id = self.context['request'].user.pk
        is_approval = ApprovalAnswerRelation.objects.filter(user=user_id,answer=answer.pk).values_list('type')
        if is_approval.exists():
            if is_approval[0][0] == 0:
                return 1
            else:
                return 0
        else:
            return 2
    def get_is_like(self,answer):
        # 判断该用户对该问题的喜欢情况,1为喜欢，0为未喜欢
        user_id = self.context['request'].user.pk
        coon = redis.Redis(connection_pool=POOL)
        is_like = coon.sismember('user:answer:like:'+str(user_id), answer.pk)
        if is_like:
            return 1
        else:
            return 0

    def get_is_collect(self,answer):
        # 判断该用户对该问题收藏情况
        user_id = self.context['request'].user.pk
        coon = redis.Redis(connection_pool=POOL)
        is_collect = coon.sismember('user:answer:collect:'+str(user_id), answer.pk)
        if is_collect:
            return 1
        else:
            return 0
    def get_is_attention_user(self,answer):
        user_id = self.context['request'].user.pk
        coon = redis.Redis(connection_pool=POOL)
        is_attention = coon.sismember('user:attention:'+str(user_id), answer.user_id)
        if is_attention:
            return 1
        else:
            return 0

    class Meta:
        model = Answer
        exclude = ['vote_number','score']


class CommentInfoSerializer(serializers.ModelSerializer):
    """评论信息序列化"""
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    user = serializers.IntegerField(source='user.pk')
    user_nick_name = serializers.CharField(source='user.nick_name')
    user_head_portrait = serializers.ImageField(source='user.head_portrait')
    is_approval = serializers.SerializerMethodField()

    # 判断用户是否赞同该评论
    def get_is_approval(self,comment):
        user_id = self.context['request'].user.pk
        coon = redis.Redis(connection_pool=POOL)
        is_approval = coon.sismember('user:comment:approval:' + str(user_id), comment.id)
        if is_approval:
            return 1
        else:
            return 0

    class Meta:
        model = Comment
        fields = ['id','user','user_nick_name','user_head_portrait',
                  'content','is_approval','approval_number','add_time']


class RevertInfoSerializer(serializers.ModelSerializer):
    """回复信息序列化"""
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    user = serializers.IntegerField(source='user.pk')
    user_nick_name = serializers.CharField(source='user.nick_name')
    user_head_portrait = serializers.ImageField(source='user.head_portrait')
    target_user_nick_name = serializers.CharField(source='target_user.nick_name')
    target_user = serializers.IntegerField(source='target_user.pk')
    is_approval = serializers.SerializerMethodField()

    # 判断用户是否赞同该回复
    def get_is_approval(self, comment):
        user_id = self.context['request'].user.pk
        coon = redis.Redis(connection_pool=POOL)
        is_approval = coon.sismember('user:revert:approval:' + str(user_id), comment.id)
        if is_approval:
            return 1
        else:
            return 0

    class Meta:
        model = Revert
        fields = ['id','user','user_nick_name','target_user','is_approval',
                  'target_user_nick_name','user_head_portrait','content','approval_number','add_time']


class AnswerBriefSerializer(serializers.ModelSerializer):
    """回答简短信息序列化器"""
    user_nick_name = serializers.CharField(source='user.nick_name')
    user_head_portrait = serializers.ImageField(source='user.head_portrait')
    modify_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Answer
        fields = ['id','user_nick_name','user_head_portrait',
                  'modify_time','content','approval_number','comment_number','like_number']


class HotQuestionSerializer(serializers.ModelSerializer):
    """热榜问题序列化器"""
    class Meta:
        model = Question
        fields = ['title','id','school']