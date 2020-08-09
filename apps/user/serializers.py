import os
import time

import redis
from rest_framework import serializers

from HotSchool.settings import domain_name, POOL
from question.models import *
from HotSchool import settings
from user.models import *


class UserInfoSerializer(serializers.ModelSerializer):
    """用户数据序列化器"""
    nick_name = serializers.CharField()
    phone = serializers.CharField(default='')
    desc = serializers.CharField(default='')
    school = serializers.CharField(source='school.name',default='')
    interests = serializers.SerializerMethodField(read_only=True,default='')
    add_time = serializers.DateField(format='%Y-%m-%d',read_only=True)

    def get_interests(self, user):
        # 兴趣为多对多，要用以下方法获得兴趣的名称
        interests = user.interest.all()
        interests = [interest.name for interest in interests]
        return interests

    class Meta:
        model = User
        fields = ['id','nick_name', 'head_portrait', 'phone', 'desc', 'school',
                   'add_time', 'interests']


class UpdateUserInfoSerializer(serializers.ModelSerializer):
    """
    用户提交信息序列化器
    必须字段:无,选要字段:nick_name,phone,desc,school,interest,interest(例子:1,2),
    """
    nick_name = serializers.CharField(min_length=2, max_length=10, required=False, error_messages={
        'min_length': '昵称最低2个字符',
        'max_length': '昵称最大10字符'
    })
    phone = serializers.CharField(min_length=11, max_length=11, required=False, error_messages={
        'min_length': '手机号最低11个字符',
        'max_length': '手机号最大11字符'
    })
    desc = serializers.CharField(min_length=5, max_length=30, required=False, error_messages={
        'min_length': '个人描述最低5个字符',
        'max_length': '个人描述最大30字符'})
    school = serializers.IntegerField(required=False)
    interest = serializers.IntegerField(required=False)


    def validate(self, attrs):
        school = attrs.get('school')
        interest = attrs.get('interest')

        if school:
            attrs['school_id'] = int(school)
            attrs.pop('school')

        if interest:
            interest = interest.split(',')
            interests_id = Interest.objects.filter(name__in=interest).values_list('id')
            interests_id_list = [i[0] for i in interests_id]
            attrs['interest'] = interests_id_list
        return attrs

    def update(self, instance, validated_data):
        new_head_portrait = validated_data.get('head_portrait',None)
        interest = validated_data.get('interest',None)
        if new_head_portrait is None:
            if interest is None:
                return User.objects.filter(id=instance.id).update(**validated_data)
            else:
                instance.interest.set(interest)
                instance.save()
                validated_data.pop('interest')
                return User.objects.filter(id=instance.id).update(**validated_data)
        else:
            image_url = instance.head_portrait.name
            # 若旧图片不是默认图片，则先移除旧图片再更新图片
            if image_url != 'headimage\default.png':
                # 更新图片之前删除旧照片
                path = settings.MEDIA_ROOT + '\\' + image_url
                os.remove(path)
            instance.head_portrait = new_head_portrait
            if interest is None:
                instance.save()
                validated_data.pop('head_portrait')
                return User.objects.filter(id=instance.id).update(**validated_data)
            else:
                # update方法无法正确更新图片的路径，必须使用save方法
                instance.interest.set(interest)
                instance.save()
                validated_data.pop('head_portrait')
                validated_data.pop('interest')
                return User.objects.filter(id=instance.id).update(**validated_data)

    class Meta:
        model = User
        fields = ['nick_name','head_portrait','phone','desc',
                    'school','interest']


class UserRecentBrowseAnswerSerializer(serializers.ModelSerializer):
    """最近浏览回答序列化器"""
    user_nick_name = serializers.CharField(source='user.nick_name')
    question_title = serializers.CharField(source='question.title')

    class Meta:
        model = Answer
        fields = ['id', 'user_nick_name', 'approval_number',
                  'comment_number','content','question_title']


class UserAttentionSerializer(serializers.ModelSerializer):
    """用户关注序列化器"""
    class Meta:
        model = User
        fields = ['id','nick_name','head_portrait','desc']


class UserQuestionCollectSerializer(serializers.ModelSerializer):
    """用户收藏的问题序列化器"""
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
            path = domain_name + '/media/headimage/anonymity.jpg'
            return path
        else:
            return domain_name + answer.user.head_portrait.url

    def get_user_nick_name(self, answer):
        if answer.is_anonymity == 1:
            return '匿名用户'
        else:
            return answer.user.nick_name

    class Meta:
        model = Answer
        fields = ['id','question_title','user_head_portrait',
                  'user_nick_name','approval_number','comment_number']


class UserRevertInfoSerializer(serializers.ModelSerializer):
    """用户的回复信息序列化"""
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    user = serializers.IntegerField(source='user.pk')
    comment_content = serializers.CharField(source='comment.content')
    question_title = serializers.CharField(source='comment.question.title')
    user_nick_name = serializers.CharField(source='user.nick_name')
    user_head_portrait = serializers.ImageField(source='user.head_portrait')
    target_user_nick_name = serializers.CharField(source='target_user.nick_name')
    target_user = serializers.IntegerField(source='target_user.pk')

    class Meta:
        model = Revert
        fields = ['id','user','user_nick_name','target_user',
                  'target_user_nick_name','user_head_portrait','comment_content',
                  'question_title','content','approval_number','add_time']


class UserAnswerInfoSerializer(serializers.ModelSerializer):
    """用户回答信息序列化"""
    user_nick_name = serializers.CharField(source='user.nick_name')
    question_title = serializers.CharField(source='question.title')
    user_head_portrait = serializers.ImageField(source='user.head_portrait')


    class Meta:
        model = Answer
        fields = ['id','user_nick_name','approval_number',
                  'comment_number','content','user_head_portrait','question_title']


class UserInfoShowSerializer(serializers.ModelSerializer):
    """用户信息展示序列化器"""
    nick_name = serializers.CharField(source='user.nick_name')
    desc = serializers.CharField(source='user.desc',default='')
    head_portrait = serializers.ImageField(source='user.head_portrait')
    collect_user_number = serializers.SerializerMethodField()
    user_be_collect_number = serializers.SerializerMethodField()

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

    class Meta:
        model = UserData
        fields = ['user','nick_name','desc','head_portrait','collect_user_number','user_be_collect_number',
                  'approval_number','like_number','collect_number','read_number']

class UserDynamicSerializer(serializers.ModelSerializer):
    """用户动态序列化器"""
    type = serializers.IntegerField()
    add_time = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    def get_content(self,obj):
        # 若type在1，2，3里面，则序列化回答，否则序列化问题
        if obj.type in [0,1,2]:
            content = UserDynamicAnswerSerializer(instance=obj.answer)
        else:
            content = UserQuestionCollectSerializer(instance=obj.question)
        return content.data

    def get_add_time(self,obj):
        time_array = time.localtime(obj.add_time)
        return time.strftime('%Y-%m-%d %H:%M',time_array)

    class Meta:
        model = UserDynamic
        fields = ['type','add_time','content',]


class UserDynamicAnswerSerializer(serializers.ModelSerializer):
    """用户动态回答序列化器"""
    question_title = serializers.CharField(source='question.title')
    user_nick_name = serializers.CharField(source='user.nick_name')

    class Meta:
        model = Answer
        fields = ['id','question_title','user_nick_name','approval_number','comment_number','content']






