import redis
from drf_haystack.serializers import HaystackSerializer

from HotSchool.settings import POOL
from food.models import Food, Flavour
from food.search_indexes import FoodIndex, FlavourIndex
from puclic import verify_serializers
from question.models import Question
from question.search_indexes import QuestionIndex
from rest_framework import serializers

from user.models import User, School
from user.search_indexes import UserIndex, SchoolIndex


class QuestionSerializer(serializers.ModelSerializer):
    """问题简短信息序列化器"""
    school = serializers.CharField(source='school.name')

    class Meta:
        model = Question
        fields = ['id', 'scan_number', 'answer_number', 'school','title']


class QuestionSearchSerializer(HaystackSerializer):
    """问题搜索序列化器"""
    object = QuestionSerializer(read_only=True)  # 只读,不可以进行反序列化

    class Meta:
        index_classes = [QuestionIndex]
        ignore_fields = ['text']


class FoodSerializer(serializers.ModelSerializer):
    """美食搜索详情序列化器"""
    image_first = serializers.URLField()
    school = serializers.CharField(source='school.name')
    score = serializers.SerializerMethodField()
    desc = serializers.SerializerMethodField()

    def get_score(self, obj):
        """将分数值舍入到小数点一位来显示"""
        if obj.vote_number < 10:
            return None
        else:
            return round(obj.score, 1)

    def get_desc(self,obj):
        """获得描述,字数大于13就截断同时添加..."""
        desc = obj.desc
        if len(desc)<15:
            return desc
        else:
            return desc[0:14]+'...'

    class Meta:
        model = Food
        fields = ['id', 'image_first', 'score', 'school','name','desc']


class FoodSearchSerializer(HaystackSerializer):
    """美食搜索返回内容序列化器"""
    object = FoodSerializer(read_only=True)

    class Meta:
        index_classes = [FoodIndex]
        ignore_fields = ['text', 'school']


class UserSerializer(serializers.ModelSerializer):
    """用户信息序列化器"""
    is_attention = serializers.SerializerMethodField()

    # 判断用户是否关注目标用户
    @verify_serializers(type=0)
    def get_is_attention(self, obj,user):
        coon = redis.Redis(connection_pool=POOL)
        is_attention = coon.sismember('attention:' + str(user.pk), obj.pk)
        if is_attention:
            return 1
        else:
            return 0

    class Meta:
        model = User
        fields = ['id', 'head_portrait', 'is_attention', 'desc','nick_name']


class UserSearchSerializer(HaystackSerializer):
    """用户搜索序列化器"""
    object = UserSerializer(read_only=True)

    class Meta:
        index_classes = [UserIndex]
        ignore_fields = ['text']


class SchoolSerializer(serializers.ModelSerializer):
    """学校信息序列化器"""

    class Meta:
        model = School
        fields = ['id', 'name']


class SchoolSearchSerializer(HaystackSerializer):
    """学校搜索序列化器"""
    object = SchoolSerializer(read_only=True)

    class Meta:
        index_classes = [SchoolIndex]
        fields = ['text']
        ignore_fields = ['text']


class FlavourSerializer(serializers.ModelSerializer):
    """口味信息序列化器"""

    class Meta:
        model = Flavour
        fields = ['id','name']


class FlavourSearchSerializer(HaystackSerializer):
    """口味搜索序列化器 """
    object = FlavourSerializer(read_only=True)

    class Meta:
        index_classes = [FlavourIndex]
        ignore_fields = ['text']
