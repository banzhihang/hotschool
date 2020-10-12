from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """用户信息表"""
    we_chat_openid = models.CharField(max_length=100, verbose_name='微信openid', default='', db_index=True)
    phone = models.CharField(verbose_name='手机号码', default='', max_length=12)
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
    head_portrait = models.URLField(verbose_name='图片url',default='',max_length=300)
    address = models.CharField(max_length=50, verbose_name='所在地', default='')
    desc = models.CharField(max_length=50, verbose_name='自我描述', default='')
    school = models.ForeignKey('School', verbose_name='学校', on_delete=models.CASCADE,default=-1)
    add_time = models.DateField(verbose_name='添加时间', auto_now_add=True)

    def __str__(self):
        return self.nick_name

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class School(models.Model):
    """学校表"""
    name = models.CharField(max_length=20, verbose_name='学校名', default='',db_index=True)
    is_campus = models.IntegerField(choices=((0, '不是校区'), (1, '是校区')), default=0, verbose_name='是否是一个校区')
    desc = models.CharField(max_length=100, verbose_name='描述', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '学校信息'
        verbose_name_plural = verbose_name


class Interest(models.Model):
    """兴趣表"""
    name = models.CharField(max_length=20, verbose_name='兴趣名称', default='')
    desc = models.CharField(max_length=50, verbose_name='描述', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '兴趣信息'
        verbose_name_plural = verbose_name


class UserData(models.Model):
    """用户创作者数据表"""
    user = models.OneToOneField('user.User', on_delete=models.CASCADE, verbose_name='用户', primary_key=True)
    approval_number = models.IntegerField(verbose_name='获赞总数', default=0)
    like_number = models.IntegerField(verbose_name='被喜欢总数', default=0)
    collect_number = models.IntegerField(verbose_name='被收藏总数', default=0)
    read_number = models.IntegerField(verbose_name='被阅读总数', default=0)
    comment_number = models.IntegerField(verbose_name='被评论数',default=0)
    answer_number = models.IntegerField(verbose_name='回答总数', default=0)

    def __str__(self):
        return self.user.nick_name

    class Meta:
        verbose_name = '用户创作者数据'
        verbose_name_plural = verbose_name


class UserDynamic(models.Model):
    """用户动态表"""
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='所属用户')
    type = models.IntegerField(choices=((0, '赞同回答'), (1, '收藏回答'), (2, '回答问题'), (3, '关注问题'), (4, '提出问题')),
                               verbose_name='操作类型',db_index=True)
    question = models.ForeignKey('question.Question', on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey('question.Answer', on_delete=models.CASCADE, default=1)
    add_time = models.FloatField('动态的创作时间的时间戳',db_index=True)

    def __str__(self):
        return self.user.nick_name

    class Meta:
        verbose_name = '用户动态'
        verbose_name_plural = verbose_name


class UserCollectFood(models.Model):
    """用户收藏美食"""
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='所属用户')
    food = models.ForeignKey('food.Food', on_delete=models.CASCADE, verbose_name='所属美食')
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True,db_index=True)

    def __str__(self):
        return self.user.nick_name

    class Meta:
        verbose_name = '用户收藏的美食'
        verbose_name_plural = verbose_name


class UserCollectQuestion(models.Model):
    """用户问题收藏"""
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='所属用户')
    question = models.ForeignKey('question.Question', on_delete=models.CASCADE, verbose_name='所属问题')
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True,db_index=True)

    def __str__(self):
        return self.user.nick_name

    class Meta:
        verbose_name = '用户收藏的问题'
        verbose_name_plural = verbose_name