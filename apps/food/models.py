from django.db import models

class Food(models.Model):
    """美食表"""
    user = models.ForeignKey('user.User',on_delete=models.CASCADE,verbose_name='该美食的作者')
    name = models.CharField(max_length=20,verbose_name='美食名称',default='')
    image_first = models.URLField(verbose_name='图片url',max_length=300)
    image_second = models.URLField(verbose_name='图片url',default='',max_length=300)
    image_third = models.URLField(verbose_name='图片url',default='',max_length=300)
    image_fourth = models.URLField(verbose_name='图片url',default='',max_length=300)
    image_fifth = models.URLField(verbose_name='图片url',default='',max_length=300)
    address_image = models.URLField(verbose_name='图片url',default='',max_length=300)
    desc = models.CharField(max_length=150,verbose_name='美食简短描述',default='')
    address = models.CharField(max_length=50,verbose_name='美食地址',default='')
    longitude = models.DecimalField(max_digits=40,decimal_places=6,verbose_name='地点的经度',default=0)
    latitude = models.DecimalField(max_digits=40,decimal_places=6,verbose_name='地点的维度',default=0)
    flavour = models.ManyToManyField('Flavour',verbose_name='美食的味道')
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    vote_number = models.IntegerField(default=0,verbose_name='投票人数')
    all_score = models.IntegerField(default=0,verbose_name='投票总分')
    score = models.FloatField(default=0.0,verbose_name='评分',db_index=True)
    school = models.ForeignKey('user.School',on_delete=models.CASCADE,verbose_name='所属学校')
    want_eat_number = models.IntegerField(default=0,verbose_name='想吃人数')
    eat_number = models.IntegerField(default=0,verbose_name='吃过人数')
    short_comment_number = models.IntegerField(default=0,verbose_name='短评数')
    discuss_number = models.IntegerField(default=0,verbose_name='讨论数')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '美食'
        verbose_name_plural = verbose_name

class Flavour(models.Model):
    """味道表"""
    id = models.IntegerField(verbose_name='id',primary_key=True)
    name = models.CharField(max_length=20, verbose_name='味道名称', default='')
    desc = models.CharField(max_length=30, verbose_name='味道描述', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '味道'
        verbose_name_plural = verbose_name


class ShortComment(models.Model):
    """短评表"""
    user = models.ForeignKey('user.User',on_delete=models.CASCADE,verbose_name='所属用户')
    food = models.ForeignKey('Food',on_delete=models.CASCADE,verbose_name='所属美食')
    approval_number = models.IntegerField(default=0,verbose_name='获赞数',db_index=True)
    content = models.CharField(max_length=300,verbose_name='短评内容')
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    score = models.IntegerField(default=1,verbose_name='该条短评的评分')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '短评'
        verbose_name_plural = verbose_name


class Discuss(models.Model):
    """讨论表"""
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='所属用户')
    food = models.ForeignKey('Food', on_delete=models.CASCADE, verbose_name='所属美食')
    title = models.CharField(max_length=30,verbose_name='内容',default='')
    approval_number = models.IntegerField(default=0,verbose_name='获赞数')
    comment_number = models.IntegerField(default=0,verbose_name='评论数',db_index=True)
    content = models.CharField(max_length=300, verbose_name='讨论内容',default='')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间', db_index=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '讨论'
        verbose_name_plural = verbose_name


class FoodComment(models.Model):
    """评论表"""
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='所属用户')
    discuss = models.ForeignKey('Discuss',on_delete=models.CASCADE, verbose_name='所属讨论')
    content = models.CharField(max_length=500,default='',verbose_name='评论内容')
    revert_number = models.IntegerField(default=0,verbose_name='回复数')
    approval_number = models.IntegerField(default=0,verbose_name='获赞数',db_index=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间', db_index=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '讨论评论'
        verbose_name_plural = verbose_name


class FoodRevert(models.Model):
    """美食讨论回复表"""
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='所属用户',related_name='user')
    comment = models.ForeignKey('FoodComment',on_delete=models.CASCADE, verbose_name='所属评论')
    target_user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='所属用户',related_name='target_user')
    content = models.CharField(max_length=500,default='',verbose_name='回复内容')
    approval_number = models.IntegerField(default=0,verbose_name='获赞数')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间', db_index=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '讨论回复'
        verbose_name_plural = verbose_name


class FoodMark(models.Model):
    """用户评分表"""
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='所属用户')
    food = models.ForeignKey('Food', on_delete=models.CASCADE, verbose_name='所属美食')
    score = models.IntegerField(default=1,verbose_name='打分的记录')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    def __str__(self):
        return self.food.name

    class Meta:
        verbose_name = '评分'
        verbose_name_plural = verbose_name


class Eated(models.Model):
    """吃过表"""
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='所属用户')
    food = models.ForeignKey('Food', on_delete=models.CASCADE, verbose_name='所属美食')

    def __str__(self):
        return self.user.nick_name

    class Meta:
        verbose_name = '吃过记录'
        verbose_name_plural = verbose_name


class WantEat(models.Model):
    """想吃表"""
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='所属用户')
    food = models.ForeignKey('Food', on_delete=models.CASCADE, verbose_name='所属美食')

    def __str__(self):
        return self.user.nick_name

    class Meta:
        verbose_name = '想吃记录'
        verbose_name_plural = verbose_name

