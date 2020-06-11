from datetime import datetime
import time

from django.db import models
import django.utils.timezone as timezone


class Question(models.Model):
    """问题表"""
    title = models.CharField(max_length=100, verbose_name="问题标题", default='')
    content = models.TextField(max_length=200, verbose_name='问题内容', default='')
    attention_number = models.IntegerField(verbose_name='关注人数', default=0)
    scan_number = models.IntegerField(verbose_name='浏览总量', default=0)
    answer_number = models.IntegerField(verbose_name='回答总数',default=0)
    campus = models.ForeignKey('user.Campus', on_delete=models.CASCADE, verbose_name='校区', default=1)
    college = models.ForeignKey('user.College', on_delete=models.CASCADE, verbose_name='学院', default=1)
    major = models.ForeignKey('user.Major', on_delete=models.CASCADE, verbose_name='专业', default=1)
    grade = models.ForeignKey('user.Grade', on_delete=models.CASCADE, verbose_name='年级', default=1)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='所属的用户')
    interest_circle = models.ManyToManyField('user.Interest',verbose_name='问题的兴趣圈子',)
    add_time = models.DateField(verbose_name='问题发布时间', auto_now_add=True)
    modify_time = models.DateTimeField(verbose_name='修改时间', default=timezone.now)

    class meta:
        verbose_name = '问题'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    """评论表"""
    type = models.IntegerField(choices=((0, '问题'), (1, '回答')), default=0)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='所属用户')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='所属问题')
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, verbose_name='所属回答', default=1)
    content = models.TextField(max_length=1000, verbose_name='用户评论', default='')
    approval_number = models.IntegerField(verbose_name='获赞数', default=0)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    modify_time = models.DateTimeField(default=timezone.now, verbose_name='内容修改时间')

    class meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name


class Revert(models.Model):
    """回复表"""
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, verbose_name='所属的评论')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='所属的用户',
                             related_name='comment_user')
    target_user = models.ForeignKey('user.User', verbose_name='被回复的人', on_delete=models.CASCADE,
                                    related_name='target_user')
    content = models.CharField(max_length=100, verbose_name='回复内容', default='')
    approval_number = models.IntegerField(verbose_name='获赞数', default=0)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    modify_time = models.DateTimeField(default=timezone.now, verbose_name='内容修改时间')

    class meta:
        verbose_name = '回复'
        verbose_name_plural = verbose_name


class Answer(models.Model):
    """回答表"""
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='所属用户')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='所属问题')
    content = models.TextField(max_length=10000, verbose_name='用户回答', default='')
    is_anonymity = models.IntegerField(choices=((0, '不匿名'), (1, '匿名')), default=0, verbose_name='是否匿名')
    vote_number = models.IntegerField(verbose_name='投票总数', default=0)
    approval_number = models.IntegerField(verbose_name='赞同数', default=0)
    comment_number = models.IntegerField(verbose_name='评论数',default=0)
    score = models.FloatField(verbose_name='得分', default=0.0)
    like_number = models.IntegerField(verbose_name='喜欢数', default=0)
    collect_number = models.IntegerField(verbose_name='收藏数', default=0)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    modify_time = models.DateTimeField(default=timezone.now, verbose_name='修改时间')

    class meta:
        verbose_name = '回答'
        verbose_name_plural = verbose_name


class HotQuestionTwentyFouryHoursOperation(models.Model):
    """24小时限定内各个问题的访问数据表"""
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='问题id')
    sacn_number = models.IntegerField(default=0, verbose_name='过去24小时浏览量')
    answer_number = models.IntegerField(default=0, verbose_name='过去24小时回答量')
    attention_number = models.IntegerField(default=0, verbose_name='过去24小时关注量')
    collect_number = models.IntegerField(default=0, verbose_name='过去24小时收藏量')
    comment_number = models.IntegerField(default=0, verbose_name='过去24小时评论量')
    score = score = models.FloatField(verbose_name='热度值', default=0.0)

    class meta:
        verbose_name = '24小时操作数据'
        verbose_name_plural = verbose_name


class HotQuestionSevenDagsOperation(models.Model):
    """7天限定内各个问题的访问数据表"""
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='问题id')
    sacn_number = models.IntegerField(default=0, verbose_name='过去7天浏览量')
    answer_number = models.IntegerField(default=0, verbose_name='过去7天回答量')
    attention_number = models.IntegerField(default=0, verbose_name='过去7天关注量')
    collect_number = models.IntegerField(default=0, verbose_name='过去7天收藏量')
    comment_number = models.IntegerField(default=0, verbose_name='过去7天评论量')
    score = models.FloatField(verbose_name='热度值', default=0.0)

    class meta:
        verbose_name = '7天操作数据'
        verbose_name_plural = verbose_name


class HotQuestionTwentyFouryHours(models.Model):
    """24小时热门问题"""
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='问题id')
    score = models.FloatField(verbose_name='问题分数', default=0.0)

    class meta:
        verbose_name = '24小时热门问题'
        verbose_name_plural = verbose_name


class HotQuestionSevenDags(models.Model):
    """7天热门问题"""
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='问题id')
    score = models.FloatField(verbose_name='问题分数', default=0.0)

    class meta:
        verbose_name = '7天热门问题'
        verbose_name_plural = verbose_name


class HotQuestionRecord(models.Model):
    """问题的上一次上热榜时间"""
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='问题id')
    last_on_hotquestion_time = models.DateField(verbose_name='上次上榜时间')

    class meta:
        verbose_name = '在榜时间'
        verbose_name_plural = verbose_name


class ApprovalAnswerRelation(models.Model):
    """回答赞同关系表"""
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='用户')
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, verbose_name='回答')
    type = models.IntegerField(choices=((0, '赞同'), (1, '反对')))

    class meta:
        verbose_name = '回答赞同关系'
        verbose_name_plural = verbose_name


class ApprovalCommentRelation(models.Model):
    """评论点赞关系"""
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='用户')
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, verbose_name='评论')

    class meta:
        verbose_name = '评论赞同关系'
        verbose_name_plural = verbose_name


class ApprovalRevertRelation(models.Model):
    """回复点赞关系"""
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='用户')
    comment = models.ForeignKey('Revert', on_delete=models.CASCADE, verbose_name='回复')

    class meta:
        verbose_name = '回复赞同关系'
        verbose_name_plural = verbose_name


class LikeRelation(models.Model):
    """喜欢关系"""
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='用户')
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, verbose_name='回答')

    class meta:
        verbose_name = '喜欢关系'
        verbose_name_plural = verbose_name


class CollectRelation(models.Model):
    """收藏关系"""
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='用户')
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, verbose_name='回答')

    class meta:
        verbose_name = '收藏关系'
        verbose_name_plural = verbose_name
