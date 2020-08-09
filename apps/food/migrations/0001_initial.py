# Generated by Django 2.2.12 on 2020-07-26 07:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0012_auto_20200725_1317'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discuss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='', max_length=1000, verbose_name='内容')),
                ('approval_number', models.IntegerField(default=0, verbose_name='获赞数')),
                ('comment_number', models.IntegerField(db_index=True, default=0, verbose_name='评论数')),
                ('content', models.CharField(max_length=300, verbose_name='讨论内容')),
                ('add_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='添加时间')),
            ],
        ),
        migrations.CreateModel(
            name='Flavour',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('name', models.CharField(default='', max_length=20, verbose_name='味道名称')),
                ('desc', models.CharField(default='', max_length=30, verbose_name='味道描述')),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20, verbose_name='美食名称')),
                ('image_first', models.ImageField(null=True, upload_to='foodimage/', verbose_name='第一张图片')),
                ('image_second', models.ImageField(null=True, upload_to='foodimage/', verbose_name='第二张图片')),
                ('image_third', models.ImageField(null=True, upload_to='foodimage/', verbose_name='第三张图片')),
                ('image_fourth', models.ImageField(null=True, upload_to='foodimage/', verbose_name='第四张图片')),
                ('image_fifth', models.ImageField(null=True, upload_to='foodimage/', verbose_name='第五张图片')),
                ('address_image', models.ImageField(null=True, upload_to='addressimage/', verbose_name='餐馆地址图片')),
                ('desc', models.CharField(default='', max_length=150, verbose_name='美食简短描述')),
                ('address', models.CharField(default='', max_length=50, verbose_name='美食地址')),
                ('longitude', models.DecimalField(decimal_places=30, default=0, max_digits=30, verbose_name='地点的经度')),
                ('latitude', models.DecimalField(decimal_places=30, default=0, max_digits=30, verbose_name='地点的维度')),
                ('add_time', models.DateField(auto_now_add=True, verbose_name='添加时间')),
                ('vote_number', models.IntegerField(default=0, verbose_name='投票人数')),
                ('vote_score', models.IntegerField(default=0, verbose_name='投票总分')),
                ('want_eat_number', models.IntegerField(default=0, verbose_name='想吃人数')),
                ('look_number', models.IntegerField(default=0, verbose_name='吃过人数')),
                ('flavour', models.ManyToManyField(to='food.Flavour', verbose_name='美食的味道')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.School', verbose_name='所属学校')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='该美食的作者')),
            ],
        ),
        migrations.CreateModel(
            name='FoodComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='', max_length=500, verbose_name='评论内容')),
                ('approval_number', models.IntegerField(db_index=True, default=0, verbose_name='获赞数')),
                ('add_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='添加时间')),
                ('discuss', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.Discuss', verbose_name='所属讨论')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='所属用户')),
            ],
        ),
        migrations.CreateModel(
            name='ShortComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_number', models.IntegerField(db_index=True, default=0, verbose_name='获赞数')),
                ('content', models.CharField(max_length=300, verbose_name='短评内容')),
                ('add_time', models.DateField(auto_now_add=True, verbose_name='添加时间')),
                ('score', models.IntegerField(default=1, verbose_name='该条短评的评分')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.Food', verbose_name='所属美食')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='所属用户')),
            ],
        ),
        migrations.CreateModel(
            name='FoodRevert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='', max_length=500, verbose_name='回复内容')),
                ('approval_number', models.IntegerField(default=0, verbose_name='获赞数')),
                ('add_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='添加时间')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.FoodComment', verbose_name='所属评论')),
                ('target_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_user', to=settings.AUTH_USER_MODEL, verbose_name='所属用户')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='所属用户')),
            ],
        ),
        migrations.AddField(
            model_name='discuss',
            name='food',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.Food', verbose_name='所属美食'),
        ),
        migrations.AddField(
            model_name='discuss',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='所属用户'),
        ),
    ]
