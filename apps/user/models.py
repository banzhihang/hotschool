from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """用户信息表"""
    we_chat_openid = models.CharField(max_length=100, verbose_name='微信openid', default='', db_index=True)
    phone = models.CharField(verbose_name='手机号码', default='', max_length=12, db_index=True)
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
    head_portrait = models.ImageField(upload_to='headimage/', default='headimage/default.png')
    address = models.CharField(max_length=50, verbose_name='所在地', default='')
    desc = models.CharField(max_length=50, verbose_name='自我描述', default='')
    campus = models.ForeignKey('Campus', verbose_name='校区',on_delete=models.CASCADE,null=True)
    school = models.ForeignKey('School', verbose_name='学校',on_delete=models.CASCADE,null=True)
    question_collect = models.ManyToManyField('question.Question', verbose_name='用户问题收藏',
                                              related_name='question_collect')
    interest = models.ManyToManyField('Interest', verbose_name='用户兴趣')
    add_time = models.DateField(verbose_name='添加时间', auto_now_add=True)

    class meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class School(models.Model):
    """学校表"""
    name = models.CharField(max_length=20, verbose_name='学校名', default='')
    desc = models.CharField(max_length=100, verbose_name='描述', default='')

    class meta:
        verbose_name = '学校'
        verbose_name_plural = verbose_name


class Campus(models.Model):
    """校区表"""
    name = models.CharField(max_length=20, verbose_name='校区名', default='')
    desc = models.CharField(max_length=100, verbose_name='描述', default='')
    school = models.ForeignKey('School',on_delete=models.CASCADE,null=True,verbose_name='所属学校')

    class meta:
        verbose_name = '校区'
        verbose_name_plural = verbose_name


class Interest(models.Model):
    """兴趣表"""
    name = models.CharField(max_length=20, verbose_name='兴趣名称', default='')
    desc = models.CharField(max_length=50, verbose_name='描述', default='')

    class meta:
        verbose_name = '兴趣'
        verbose_name_plural = verbose_name

class UserData(models.Model):
    """用户创作数据表"""
    user = models.OneToOneField('user.User',on_delete=models.CASCADE,verbose_name='用户',primary_key=True)
    approval_number = models.IntegerField(verbose_name='获赞总数',default=0)
    like_number = models.IntegerField(verbose_name='被喜欢总数',default=0)
    collect_number = models.IntegerField(verbose_name='被收藏总数',default=0)
    read_number = models.IntegerField(verbose_name='被阅读总数',default=0)
    answer_number = models.IntegerField(verbose_name='回答总数',default=0)

    class meta:
        verbose_name = '用户创作数据'
        verbose_name_plural = verbose_name

class UserDynamic(models.Model):
    """用户动态表"""
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='所属用户')
    type = models.IntegerField(choices=((0,'赞同回答'),(1,'收藏回答'),(2,'回答问题'),(3,'关注问题'),(4,'提出问题')),verbose_name='操作类型')
    question = models.ForeignKey('question.Question',on_delete=models.CASCADE,default=1)
    answer = models.ForeignKey('question.Answer',on_delete=models.CASCADE,default=1)
    add_time = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')

    class meta:
        verbose_name = '用户动态'
        verbose_name_plural = verbose_name