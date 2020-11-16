from django.db import models


class AnswerDraft(models.Model):
    """回答草稿表"""
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='所属的用户')
    question = models.ForeignKey('question.Question', on_delete=models.CASCADE, verbose_name='所属问题')
    is_anonymity = models.IntegerField(choices=((0, '不匿名'), (1, '匿名')), default=0, verbose_name='是否匿名')
    content = models.TextField(max_length=100000, verbose_name='用户回答', default='')
    abstract = models.CharField(max_length=18,verbose_name="草稿摘要",default='')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    modify_time = models.DateTimeField(auto_now = True, verbose_name='修改时间',db_index=True)

    def __str__(self):
        return self.user.nick_name

    class Meta:
        verbose_name = '回答草稿'
        verbose_name_plural = verbose_name


class FoodDraft(models.Model):
    """美食草稿表"""
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='该美食的作者')
    name = models.CharField(max_length=20, verbose_name='美食名称',db_index=True)
    image_first = models.URLField(verbose_name='图片url',null=True)
    image_second = models.URLField(verbose_name='图片url',null=True)
    image_third = models.URLField(verbose_name='图片url', null=True)
    image_fourth = models.URLField(verbose_name='图片url',null=True)
    image_fifth = models.URLField(verbose_name='图片url', null=True)
    address_image = models.URLField(verbose_name='图片url', null=True)
    desc = models.CharField(max_length=150, verbose_name='美食简短描述',null=True)
    address = models.CharField(max_length=50, verbose_name='美食地址',db_index=True)
    longitude = models.DecimalField(max_digits=40, decimal_places=6, verbose_name='地点的经度')
    latitude = models.DecimalField(max_digits=40, decimal_places=6, verbose_name='地点的维度')
    flavour = models.ManyToManyField('food.Flavour', verbose_name='美食的味道')
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间',db_index=True)
    school = models.ForeignKey('user.School', on_delete=models.CASCADE, verbose_name='所属学校',null=True)

    def __str__(self):
        return self.user.nick_name

    class Meta:
        verbose_name = '美食草稿'
        verbose_name_plural = verbose_name

