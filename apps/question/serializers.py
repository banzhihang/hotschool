from rest_framework import serializers

from HotSchool.settings import domain_name
from .models import *


class QuestionInfoSerializer(serializers.ModelSerializer):
    """问题信息序列化"""
    add_time = serializers.DateField(format='%Y-%m-%d')
    modify_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
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
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    modify_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
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
        user_id = self.context['request'].user.pk
        is_approval = ApprovalAnswerRelation.objects.filter(user=user_id,answer=answer.pk).values_list('type')
        if is_approval:
            if is_approval[0][0] == 0:
                return '赞同'
            else:
                return '反对'
        else:
            return '未表态'
    def get_is_like(self,answer):
        user_id = self.context['request'].user.pk
        is_like = LikeRelation.objects.filter(user=user_id,answer=answer.pk).values_list()
        if is_like:
            return '已喜欢'
        else:
            return '未喜欢'

    def get_is_collect(self,answer):
        user_id = self.context['request'].user.pk
        is_collect = CollectRelation.objects.filter(user=user_id, answer=answer.pk).values_list()
        if is_collect:
            return '已收藏'
        else:
            return '未收藏'
    def get_is_attention_user(self,answer):
        user_id = self.context['request'].user.pk
        is_collect = AttentionRelation.objects.filter(user=user_id, target_user=answer.user_id).values_list()
        if is_collect:
            return '已关注'
        else:
            return '未关注'

    class Meta:
        model = Answer
        exclude = ['vote_number','score']


class CommentInfoSerializer(serializers.ModelSerializer):
    """评论信息序列化"""
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    user = serializers.IntegerField(source='user.pk')
    user_nick_name = serializers.CharField(source='user.nick_name')
    user_head_portrait = serializers.ImageField(source='user.head_portrait')



    class Meta:
        model = Comment
        fields = ['id','user','user_nick_name','user_head_portrait',
                  'content','approval_number','add_time']


class RevertInfoSerializer(serializers.ModelSerializer):
    """回复信息序列化"""
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    user = serializers.IntegerField(source='user.pk')
    user_nick_name = serializers.CharField(source='user.nick_name')
    user_head_portrait = serializers.ImageField(source='user.head_portrait')
    target_user_nick_name = serializers.CharField(source='target_user.nick_name')
    target_user = serializers.IntegerField(source='target_user.pk')

    class Meta:
        model = Revert
        fields = ['id','user','user_nick_name','target_user',
                  'target_user_nick_name','user_head_portrait','content','approval_number','add_time']