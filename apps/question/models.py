from django.db import models
import django.utils.timezone as timezone


class Question(models.Model):
    """问题表"""
    title = models.CharField(max_length=100, verbose_name="问题标题", default='')
    content = models.TextField(max_length=200, verbose_name='问题内容', default='')
    attention_number = models.IntegerField(verbose_name='关注人数', default=0)
    scan_number = models.IntegerField(verbose_name='浏览总量', default=0)
    answer_number = models.IntegerField(verbose_name='回答总数',default=0)
    is_anonymity = models.IntegerField(choices=((0, '不匿名'), (1, '匿名')), default=0, verbose_name='是否匿名')
    school = models.ForeignKey('user.School',on_delete=models.CASCADE,verbose_name='所属学校')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='所属的用户')
    interest_circle = models.ManyToManyField('user.Interest',verbose_name='问题的兴趣圈子',)
    add_time = models.DateField(verbose_name='问题发布时间', auto_now_add=True)
    modify_time = models.DateTimeField(verbose_name='修改时间',auto_now = True)

    class Meta:
        verbose_name = '问题'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    """评论表"""
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='所属用户')
    is_anonymity = models.IntegerField(choices=((0, '不匿名'), (1, '匿名')), default=0, verbose_name='是否匿名')
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, verbose_name='所属回答')
    content = models.TextField(max_length=1000, verbose_name='用户评论', default='')
    revert_number = models.IntegerField(verbose_name='回复数数', default=0)
    approval_number = models.IntegerField(verbose_name='获赞数', default=0,db_index=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间',db_index=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name


class Revert(models.Model):
    """回复表"""
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, verbose_name='所属的评论')
    is_user_anonymity = models.IntegerField(choices=((0, '不匿名'), (1, '匿名')), default=0, verbose_name='用户是否匿名')
    is_target_user_anonymity = models.IntegerField(choices=((0, '不匿名'), (1, '匿名')), default=0, verbose_name='目标用户是否匿名')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='所属的用户',
                             related_name='revert_comment_user')
    target_user = models.ForeignKey('user.User', verbose_name='被回复的人', on_delete=models.CASCADE,
                                    related_name='revert_target_user')
    content = models.CharField(max_length=100, verbose_name='回复内容', default='')
    approval_number = models.IntegerField(verbose_name='获赞数', default=0)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间',db_index=True)

    class Meta:
        verbose_name = '回复'
        verbose_name_plural = verbose_name


class Answer(models.Model):
    """回答表"""
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='所属用户')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='所属问题')
    content = models.TextField(max_length=100000, verbose_name='用户回答', default='')
    is_anonymity = models.IntegerField(choices=((0, '不匿名'), (1, '匿名')), default=0, verbose_name='是否匿名')
    vote_number = models.IntegerField(verbose_name='投票总数', default=0)
    approval_number = models.IntegerField(verbose_name='赞同数', default=0)
    comment_number = models.IntegerField(verbose_name='评论数',default=0)
    score = models.FloatField(verbose_name='得分', default=0.0)
    like_number = models.IntegerField(verbose_name='喜欢数', default=0)
    collect_number = models.IntegerField(verbose_name='收藏数', default=0)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间',db_index=True)
    modify_time = models.DateTimeField(verbose_name='修改时间',auto_now = True)

    class Meta:
        verbose_name = '回答'
        verbose_name_plural = verbose_name










