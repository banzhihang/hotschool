from rest_framework import serializers

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

    class Meta:
        model = Answer
        fields = "__all__"


class CommentInfoSerializer(serializers.ModelSerializer):
    """评论信息序列化"""
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    modify_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Comment
        fields = "__all__"


class RevertInfoSerializer(serializers.ModelSerializer):
    """回复信息序列化"""
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    modify_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Revert
        fields = "__all__"