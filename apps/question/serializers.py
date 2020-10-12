import redis
from django.db.models import F
from rest_framework import serializers

from HotSchool.settings import POOL, ANONYMITY_USER_HEAD_IMAGE
from draft.models import AnswerDraft
from puclic import verify_serializers
from user.models import UserCollectQuestion
from .extra import add_user_operation_data, get_hot_question_image
from .models import *


class QuestionInfoSerializer(serializers.ModelSerializer):
    """问题信息序列化"""
    add_time = serializers.DateField(format='%Y-%m-%d')
    modify_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    school = serializers.CharField(source='school.name')
    is_collect = serializers.SerializerMethodField()
    has_answer_id = serializers.SerializerMethodField()
    has_draft_id = serializers.SerializerMethodField()

    @verify_serializers(type=0)
    def get_is_collect(self, obj, user=None):
        # 判断该用户有没有收藏该问题
        is_collect = UserCollectQuestion.objects.filter(user_id=user.pk, question_id=obj.pk)
        if is_collect.exists():
            return 1
        else:
            return 0

    @verify_serializers(type=-1)
    def get_has_answer_id(self, obj, user=None):
        # 判断该用户在该问题下有没有回答
        answer_set = Answer.objects.filter(user_id=user.pk, question_id=obj.pk).values_list('id')
        if answer_set:
            return answer_set[0][0]
        else:
            return -1

    @verify_serializers(type=-1)
    def get_has_draft_id(self, obj, user=None):
        # 判断该用户在该问题下有没有草稿
        draft_set = AnswerDraft.objects.filter(user_id=user.pk, question_id=obj.pk).values_list('id')
        if draft_set:
            return draft_set[0][0]
        else:
            return -1

    class Meta:
        model = Question
        exclude = ['is_anonymity', 'interest_circle']


class PostQuestionSerializer(serializers.ModelSerializer):
    """
    发布问题序列化器
    必要参数:title(问题标题),school(学校id)
    选要参数:content(问题内容)
    """
    title = serializers.CharField(required=True, min_length=4, max_length=50, allow_blank=False, error_messages={
        'min_length': '问题最少4个字',
        'max_length': '问题最大50个字',
        'allow_blank': '标题不允许为空'
    })
    content = serializers.CharField(required=False)

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        return attrs

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    class Meta:
        model = Question
        fields = ['title', 'content', 'school']


class AnswerInfoSerializer(serializers.ModelSerializer):
    """回答信息序列化"""
    modify_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    question_title = serializers.CharField(source='question.title')
    approval_number = serializers.SerializerMethodField()
    like_number = serializers.SerializerMethodField()
    collect_number = serializers.SerializerMethodField()
    user_head_portrait = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    user_nick_name = serializers.SerializerMethodField()
    user_desc = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()
    is_approval = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    is_collect = serializers.SerializerMethodField()
    is_attention_user = serializers.SerializerMethodField()
    has_answer_id = serializers.SerializerMethodField()

    def get_user_head_portrait(self, answer):
        if answer.is_anonymity:
            return ANONYMITY_USER_HEAD_IMAGE
        else:
            return answer.user.head_portrait

    def get_user_nick_name(self, answer):
        if answer.is_anonymity:
            return '匿名用户'
        else:
            return answer.user.nick_name

    def get_user(self, answer):
        if answer.is_anonymity:
            return None
        else:
            return answer.user_id

    @verify_serializers(type=0)
    def get_is_author(self, answer, user):
        # 判断该用户是不是作者
        if user.pk == answer.user.pk:
            return 1
        else:
            return 0

    def get_user_desc(self, answer):
        if answer.is_anonymity:
            return None
        else:
            return answer.user.desc

    def get_approval_number(self, answer):
        # 获取获赞数，先从redis 获取，获取不到载从数据库获取
        coon = redis.Redis(connection_pool=POOL)
        data = coon.hget('ad:' + str(answer.pk), 'approval')
        if data:
            return int(data)
        else:
            return answer.approval_number

    def get_like_number(self, answer):
        coon = redis.Redis(connection_pool=POOL)
        data = coon.bitcount('al:' + str(answer.pk), start=0, end=-1)
        return data

    def get_collect_number(self, answer):
        coon = redis.Redis(connection_pool=POOL)
        data = coon.hget('ad:' + str(answer.pk), 'collect')
        if data:
            return int(data)
        else:
            return answer.collect_number

    @verify_serializers(type=2)
    def get_is_approval(self, answer, user):
        # 判断用户的赞同情况0反对,1赞同,2未表态
        coon = redis.Redis(connection_pool=POOL)
        is_approval = coon.sismember('approval:' + str(user.pk), 'a:' + str(answer.id) + ':' + '1')
        is_oppose = coon.sismember('approval:' + str(user.pk), 'a:' + str(answer.id) + ':' + '0')
        if is_approval:
            return 1
        elif is_oppose:
            return 0
        else:
            return 2

    @verify_serializers(type=0)
    def get_is_like(self, answer, user):
        # 判断该用户对该问题的喜欢情况,1为喜欢，0为未喜欢
        coon = redis.Redis(connection_pool=POOL)
        is_like = coon.getbit('al:' + str(answer.pk), user.pk)
        if is_like:
            return 1
        else:
            return 0

    @verify_serializers(type=0)
    def get_is_collect(self, answer, user):
        # 判断该用户对该回答收藏情况
        coon = redis.Redis(connection_pool=POOL)
        is_collect = coon.sismember('collect:' + str(user.pk), answer.pk)
        if is_collect:
            return 1
        else:
            return 0

    @verify_serializers(type=0)
    def get_is_attention_user(self, answer, user):
        # 判断该用户是否关注该作者
        coon = redis.Redis(connection_pool=POOL)
        is_attention = coon.sismember('attention:' + str(user.pk), answer.user_id)
        if is_attention:
            return 1
        else:
            return 0

    @verify_serializers(type=-1)
    def get_has_answer_id(self, answer, user):
        # 看看该问题下是否有此人的回答,有就返回该回答id,没有就返回-1
        answer_set = Answer.objects.filter(question_id=answer.question_id, user_id=user.pk).values_list('id')
        if answer_set:
            return answer_set[0][0]
        else:
            return -1

    class Meta:
        model = Answer
        exclude = ['vote_number', 'score', 'add_time']


class PostAndUpdateAnswerSerializer(serializers.ModelSerializer):
    """
    回答发布序列化器
    必要参数:content(回答内容) is_anonymity(是否匿名回答) question(所属问题id)
    选要参数:无
    """
    content = serializers.CharField(required=True, min_length=1, max_length=100000, allow_blank=False, error_messages={
        'min_length': '回答最少4个字',
        'max_length': '回答最大100000个字',
        'allow_blank': '标题不允许为空'
    })
    is_anonymity = serializers.IntegerField(required=True, error_messages={
        'required': '此选项不允许为空'
    })

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        return attrs

    def create(self, validated_data):
        question = validated_data.get('question')
        return Answer.objects.create(**validated_data), question

    def update(self, instance, validated_data):
        return Answer.objects.filter(pk=instance.pk).update(**validated_data)

    class Meta:
        model = Answer
        fields = ['content', 'question', 'is_anonymity']


class CommentInfoSerializer(serializers.ModelSerializer):
    """评论信息序列化"""
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    user = serializers.IntegerField(source='user.pk')
    user_nick_name = serializers.SerializerMethodField()
    user_head_portrait = serializers.SerializerMethodField()
    is_approval = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

    # 判断用户是否赞同该评论
    @verify_serializers(type=0)
    def get_is_approval(self, comment, user):
        coon = redis.Redis(connection_pool=POOL)
        is_approval = coon.sismember('approval:' + str(user.pk), 'c:' + str(comment.id))
        if is_approval:
            return 1
        else:
            return 0

    @verify_serializers(type=0)
    def get_is_author(self, comment, user):
        # 判断该用户是不是作者
        if comment.user.pk == user.pk:
            return 1
        else:
            return 0

    def get_user_nick_name(self, comment):
        if comment.is_anonymity:
            return '匿名用户'
        else:
            return comment.user.nick_name

    def get_user_head_portrait(self, comment):
        if comment.is_anonymity:
            return ANONYMITY_USER_HEAD_IMAGE
        else:
            return comment.user.head_portrait

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_nick_name', 'user_head_portrait', 'revert_number',
                  'content', 'is_approval', 'is_author', 'approval_number', 'add_time', 'is_anonymity']


class RevertInfoSerializer(serializers.ModelSerializer):
    """回复信息序列化"""
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    user = serializers.IntegerField(source='user.pk')
    user_nick_name = serializers.SerializerMethodField()
    user_head_portrait = serializers.SerializerMethodField()
    target_user_nick_name = serializers.SerializerMethodField()
    target_user = serializers.IntegerField(source='target_user.pk')
    is_approval = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

    # 判断用户是否赞同该回复
    @verify_serializers(type=0)
    def get_is_approval(self, comment, user):
        coon = redis.Redis(connection_pool=POOL)
        is_approval = coon.sismember('approval:' + str(user.pk), 'r:' + str(comment.id))
        if is_approval:
            return 1
        else:
            return 0

    @verify_serializers(type=0)
    def get_is_author(self, revert, user):
        if revert.user.pk == user.pk:
            return 1
        else:
            return 0

    def get_user_nick_name(self, revert):
        if revert.is_user_anonymity:
            return '匿名用户'
        else:
            return revert.user.nick_name

    def get_user_head_portrait(self, revert):
        if revert.is_user_anonymity:
            return ANONYMITY_USER_HEAD_IMAGE
        else:
            return revert.user.head_portrait

    def get_target_user_nick_name(self, revert):
        if revert.is_target_user_anonymity:
            return '匿名用户'
        else:
            return revert.target_user.nick_name

    class Meta:
        model = Revert
        fields = ['id', 'user', 'user_nick_name', 'target_user', 'is_approval', 'is_author', 'is_user_anonymity',
                  'is_target_user_anonymity', 'target_user_nick_name', 'user_head_portrait', 'content',
                  'approval_number', 'add_time']


class AnswerBriefSerializer(serializers.ModelSerializer):
    """回答简短信息序列化器"""
    user_nick_name = serializers.CharField(source='user.nick_name')
    user_head_portrait = serializers.URLField(source='user.head_portrait')
    modify_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Answer
        fields = ['id', 'user_nick_name', 'user_head_portrait', 'first_image',
                  'modify_time', 'abstract', 'approval_number', 'comment_number', 'like_number']


class HotQuestionSerializer(serializers.ModelSerializer):
    """热榜问题序列化器"""
    school = serializers.CharField(source='school.name')
    image = serializers.SerializerMethodField()

    # 获得热榜问题的配图
    def get_image(self, obj):
        res = get_hot_question_image(obj)
        if res:
            return res
        else:
            return None

    class Meta:
        model = Question
        fields = ['title', 'id', 'school', 'image']


class CreateCommentSerializer(serializers.ModelSerializer):
    """
    发布评论序列化器
    必要参数:answer(评论所属回答id) content(评论内容)
    """
    content = serializers.CharField(required=True, error_messages={'blank': '内容不允许为空'})

    def create(self, validated_data):
        answer = validated_data.get('answer')
        return Comment.objects.create(**validated_data), answer.user_id, answer.question_id

    def validate(self, attrs):
        answer = attrs.get('answer')
        # 若该回答的作者选择了匿名回答,同时发布该评论的人是该作者,则这条评论的is_anonymity改为1,即匿名发布该评论
        if answer.is_anonymity == 1:
            if self.context['request'].user.pk == answer.user_id:
                attrs['is_anonymity'] = 1
        # 回答的comment_number字段加一
        answer.comment_number = F('comment_number') + 1
        answer.save()
        # 添加对应回答的作者的创作数据
        add_user_operation_data('comment', answer.user.pk, 'add')
        attrs['user'] = self.context['request'].user
        return attrs

    class Meta:
        model = Comment
        fields = ['answer', 'content']


class CreateRevertSerializer(serializers.ModelSerializer):
    """
    发布回复序列化器
    必要参数:target_user(回复目标用户),comment(回复所属评论) content(回复内容)
    """
    content = serializers.CharField(required=True, error_messages={'blank': '内容不允许为空'})

    def validate(self, attrs):
        comment = attrs['comment']
        target_user = attrs['target_user']
        # 查询出该评论对应回答是否匿名以及作者的id
        answer_user_id, answer_is_anonymity = comment.answer.user_id, comment.answer.is_anonymity

        # (1)若该评论对应回答是匿名,则根据target_user_set.pk和answer_user_id来判断目标用户是不是作者,
        # 是的话该回复的is_target_user_anonymity字段置为1.(2)若添加该条回复的用户id等于回答作者的id,
        # 则该条回复的is_user_anonymity字段置为1
        if answer_is_anonymity:
            if target_user.pk == answer_user_id:
                attrs['is_target_user_anonymity'] = 1
            if self.context['request'].user.pk == answer_user_id:
                attrs['is_user_anonymity'] = 1
        # 将对应评论的回复数加一
        comment.revert_number = F('revert_number') + 1
        comment.save()
        attrs['user'] = self.context['request'].user
        return attrs

    def create(self, validated_data):
        target_user_id = validated_data['target_user'].pk
        return Revert.objects.create(**validated_data), target_user_id

    class Meta:
        model = Revert
        fields = ['content', 'target_user', 'comment']
