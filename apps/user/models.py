from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone

from datetime import datetime


class User(AbstractUser):
    """用户信息表"""
    we_chat_openid = models.CharField(max_length=100, verbose_name='微信openid', default='', db_index=True)
    we_chat_unionid = models.CharField(max_length=100, verbose_name='微信unionid', default='')
    phone = models.CharField(verbose_name='手机号码', default='', max_length=12, db_index=True)
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
    head_portrait = models.ImageField(upload_to='headimage/', default='headimage/default.png')
    address = models.CharField(max_length=50, verbose_name='所在地', default='')
    desc = models.CharField(max_length=50, verbose_name='自我描述', default='')
    campus = models.ForeignKey('Campus', verbose_name='校区',on_delete=models.CASCADE,null=True)
    college = models.ForeignKey('College', on_delete=models.CASCADE, verbose_name='学院',null=True)
    major = models.ForeignKey('Major', verbose_name='专业', on_delete=models.CASCADE,null=True)
    grade = models.ForeignKey('Grade', verbose_name='年级', on_delete=models.CASCADE,null=True)
    question_collect = models.ManyToManyField('question.Question', verbose_name='用户问题收藏',
                                              related_name='question_collect',null=True)
    answer_collect = models.ManyToManyField('question.Answer', verbose_name='用户回答收藏',
                                            related_name='answer_collect',null=True)
    attention = models.ManyToManyField('self', verbose_name='用户关注', related_name='attention',null=True)

    interest = models.ManyToManyField('Interest', verbose_name='用户兴趣',null=True)
    add_time = models.DateField(verbose_name='添加时间', auto_now_add=True)

    class meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class Grade(models.Model):
    """年级表"""
    grade = models.IntegerField(verbose_name='年级')
    desc = models.CharField(max_length=50, verbose_name='描述')

    class meta:
        verbose_name = '年级'
        verbose_name_plural = verbose_name


class Campus(models.Model):
    """校区表"""
    name = models.CharField(max_length=20, verbose_name='校区名', default='')
    desc = models.CharField(max_length=100, verbose_name='描述', default='')
    school = models.CharField(max_length=30, verbose_name='所属学校', default='')

    class meta:
        verbose_name = '校区'
        verbose_name_plural = verbose_name


class College(models.Model):
    """学院表"""
    name = models.CharField(max_length=20, verbose_name='学院名', default='')
    desc = models.CharField(max_length=100, verbose_name='描述', default='')
    campus = models.ForeignKey('Campus', on_delete=models.CASCADE)

    class meta:
        verbose_name = '学院'
        verbose_name_plural = verbose_name


class Major(models.Model):
    """专业表"""
    name = models.CharField(max_length=50, verbose_name='专业名', default='')
    desc = models.CharField(max_length=100, verbose_name='描述', default='')
    college = models.ForeignKey('College', on_delete=models.CASCADE)

    class meta:
        verbose_name = '专业'
        verbose_name_plural = verbose_name


class Interest(models.Model):
    """兴趣表"""
    name = models.CharField(max_length=20, verbose_name='兴趣名称', default='')
    desc = models.CharField(max_length=50, verbose_name='描述', default='')

    class meta:
        verbose_name = '兴趣'
        verbose_name_plural = verbose_name


class RecentBrowseQuestion(models.Model):
    """最近浏览问题记录表"""
    question = models.ForeignKey('question.Question',on_delete=models.CASCADE,verbose_name='问题')
    add_time = models.DateTimeField(auto_now=True, verbose_name='浏览时间')
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class meta:
        verbose_name = '最近浏览问题'
        verbose_name_plural = verbose_name


class RecentBrowseAnswer(models.Model):
    """最近浏览回答记录表"""
    answer = models.ForeignKey('question.Answer',on_delete=models.CASCADE,verbose_name='回答')
    add_time = models.DateTimeField(auto_now=True, verbose_name='浏览时间')
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class meta:
        verbose_name = '最近浏览回答'
        verbose_name_plural = verbose_name
