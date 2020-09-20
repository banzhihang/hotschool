import redis

from rest_framework import serializers

from HotSchool.settings import POOL, domain_name
from question.models import Answer, Question


class AnswerRecommendSerializer(serializers.ModelSerializer):
    """推荐回答序列化器"""
    question_title = serializers.CharField(source='question.title')
    user_head_portrait = serializers.SerializerMethodField()
    user_nick_name = serializers.SerializerMethodField()
    approval_number = serializers.SerializerMethodField()
    type = serializers.IntegerField(default=0)

    def get_user_head_portrait(self, answer):
        if answer.is_anonymity:
            path = domain_name + '/media/headimage/anonymity.jpg'
            return path
        else:
            return domain_name + answer.user.head_portrait.url

    def get_user_nick_name(self, answer):
        if answer.is_anonymity:
            return '匿名用户'
        else:
            return answer.user.nick_name

    def get_approval_number(self, answer):
        # 获取获赞数，先从redis 获取，获取不到载从数据库获取
        coon = redis.Redis(connection_pool=POOL)
        data = coon.hget('ad:' + str(answer.pk), 'approval')
        if data:
            return int(data)
        else:
            return answer.approval_number

    class Meta:
        model = Answer
        fields = ['type','id','question_title','user_head_portrait','user_nick_name','approval_number',
                  'comment_number','abstract','first_image']


class QuestionRecommendSerializer(serializers.ModelSerializer):
    """推荐问题序列化器"""
    type = serializers.IntegerField(default=1)
    class Meta:
        model = Question
        fields = ['type','id','title','content']


class LatestQuestionSerializer(serializers.ModelSerializer):
    """最新问题序列化器"""
    class Meta:
        model = Question
        fields = ['id','title','content']
