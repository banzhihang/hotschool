import os

from rest_framework import serializers

from HotSchool import settings
from user.models import *


class UserInfoSerializer(serializers.ModelSerializer):
    """用户数据序列化器"""
    nick_name = serializers.CharField(min_length=2,max_length=10,required=False,error_messages={
        'min_length':'昵称最低2个字符',
        'max_length':'昵称最大10字符'
    })
    phone = serializers.CharField(min_length=11,max_length=11,required=False,error_messages={
        'min_length':'手机号最低11个字符',
        'max_length':'手机号最大11字符'
    })
    desc = serializers.CharField(min_length=5,max_length=30,required=False,error_messages={
        'min_length': '个人描述最低5个字符',
        'max_length': '个人描述最大30字符'
    })
    campus = serializers.CharField(required=False,source='campus.name')
    college = serializers.CharField(required=False,source='college.name')
    major = serializers.CharField(required=False,source='major.name')
    grade = serializers.IntegerField(required=False,source='grade.grade')
    interests = serializers.SerializerMethodField(read_only=True)
    add_time = serializers.DateField(format='%Y-%m-%d',read_only=True)


    def validate(self, attrs):
        # 由于以下四个值为外键，经过反序列化。值变成了字典。
        # 以下代码将字典变成一个整数id(获得的字典的value为名称，要转换成id存储)
        campus = attrs.get('campus',None)
        college = attrs.get('college',None)
        major = attrs.get('major',None)
        grade = attrs.get('grade',None)

        if campus:
            campus_name = campus['name']
            campus_id = Campus.objects.filter(name=campus_name).values_list('id')[0][0]
            attrs['campus'] = campus_id
        if college:
            college_name = college['name']
            college_id = College.objects.filter(name=college_name).values_list('id')[0][0]
            attrs['college'] = college_id
        if major:
            major_name = major['name']
            major_id = Major.objects.filter(name=major_name).values_list('id')[0][0]
            attrs['major'] = major_id
        if grade:
            grade_name = grade['grade']
            grade_id = Grade.objects.filter(grade=grade_name).values_list('id')[0][0]
            attrs['grade'] = grade_id

        return attrs

    def get_interests(self, user):
        # 兴趣为多对多，要用以下方法获得兴趣的名称
        interests = user.interest.all()
        interests = [interest.name for interest in interests]
        return interests


    def update(self, instance, validated_data):
        image_url = instance.head_portrait.name
        # 若图片不是默认图片，则先移除旧图片再更新图片
        if image_url != 'headimage\default.png':
            # 更新图片之前删除旧照片
            path = settings.MEDIA_ROOT + '\\' + image_url
            os.remove(path)
        # update方法无法正确更新图片的路径，必须使用save方法
        instance.head_portrait = validated_data.get('head_portrait')
        instance.save()
        validated_data.pop('head_portrait')
        return User.objects.filter(id=instance.id).update(**validated_data)

    class Meta:
        model = User
        fields = ['id','nick_name', 'head_portrait', 'phone', 'desc','campus', 'college',
                  'major', 'grade', 'add_time', 'interests']


class UserRecentBrowseQuestionSerializer(serializers.ModelSerializer):
    """最近浏览问题序列化器"""
    add_time = serializers.DateTimeField(format='%Y-%m-%d')
    question = serializers.SerializerMethodField()

    def get_question(self, obj):
        content = {'id': obj.question_id,
                   'user': obj.question.user.nick_name,
                   'title': obj.question.title,
                   'content': obj.question.content,
                   'answer_number': obj.question.answer_number,
                   'attention_number': obj.question.attention_number,
                   }
        return content

    class Meta:
        model = RecentBrowseQuestion
        fields = ['add_time', 'question']


class UserRecentBrowseAnswerSerializer(serializers.ModelSerializer):
    """最近浏览回答序列化器"""
    add_time = serializers.DateTimeField(format='%Y-%m-%d')
    answer = serializers.SerializerMethodField()

    def get_answer(self, obj):
        content = {'id': obj.answer_id,
                   'user': obj.answer.user.nick_name,
                   'content': obj.answer.content,
                   'approval_number':obj.answer.approval_number,
                   'comment_number':obj.answer.comment_number
                   }
        return content

    class Meta:
        model = RecentBrowseAnswer
        fields = ['add_time', 'answer']
