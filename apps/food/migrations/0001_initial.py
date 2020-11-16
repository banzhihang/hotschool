# Generated by Django 2.2.12 on 2020-11-01 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discuss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=30, verbose_name='内容')),
                ('approval_number', models.IntegerField(default=0, verbose_name='获赞数')),
                ('comment_number', models.IntegerField(db_index=True, default=0, verbose_name='评论数')),
                ('content', models.CharField(default='', max_length=300, verbose_name='讨论内容')),
                ('add_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '讨论',
                'verbose_name_plural': '讨论',
            },
        ),
        migrations.CreateModel(
            name='Eated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '吃过记录',
                'verbose_name_plural': '吃过记录',
            },
        ),
        migrations.CreateModel(
            name='Flavour',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('name', models.CharField(default='', max_length=20, verbose_name='味道名称')),
                ('desc', models.CharField(default='', max_length=30, verbose_name='味道描述')),
            ],
            options={
                'verbose_name': '味道',
                'verbose_name_plural': '味道',
            },
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20, verbose_name='美食名称')),
                ('image_first', models.URLField(max_length=300, verbose_name='图片url')),
                ('image_second', models.URLField(default='', max_length=300, verbose_name='图片url')),
                ('image_third', models.URLField(default='', max_length=300, verbose_name='图片url')),
                ('image_fourth', models.URLField(default='', max_length=300, verbose_name='图片url')),
                ('image_fifth', models.URLField(default='', max_length=300, verbose_name='图片url')),
                ('address_image', models.URLField(default='', max_length=300, verbose_name='图片url')),
                ('desc', models.CharField(default='', max_length=150, verbose_name='美食简短描述')),
                ('address', models.CharField(default='', max_length=50, verbose_name='美食地址')),
                ('longitude', models.DecimalField(decimal_places=6, default=0, max_digits=40, verbose_name='地点的经度')),
                ('latitude', models.DecimalField(decimal_places=6, default=0, max_digits=40, verbose_name='地点的维度')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('vote_number', models.IntegerField(default=0, verbose_name='投票人数')),
                ('all_score', models.IntegerField(default=0, verbose_name='投票总分')),
                ('score', models.FloatField(db_index=True, default=0.0, verbose_name='评分')),
                ('want_eat_number', models.IntegerField(default=0, verbose_name='想吃人数')),
                ('eat_number', models.IntegerField(default=0, verbose_name='吃过人数')),
                ('short_comment_number', models.IntegerField(default=0, verbose_name='短评数')),
                ('discuss_number', models.IntegerField(default=0, verbose_name='讨论数')),
            ],
            options={
                'verbose_name': '美食',
                'verbose_name_plural': '美食',
            },
        ),
        migrations.CreateModel(
            name='FoodComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='', max_length=500, verbose_name='评论内容')),
                ('revert_number', models.IntegerField(default=0, verbose_name='回复数')),
                ('approval_number', models.IntegerField(db_index=True, default=0, verbose_name='获赞数')),
                ('add_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '讨论评论',
                'verbose_name_plural': '讨论评论',
            },
        ),
        migrations.CreateModel(
            name='FoodMark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=1, verbose_name='打分的记录')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '评分',
                'verbose_name_plural': '评分',
            },
        ),
        migrations.CreateModel(
            name='FoodRevert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='', max_length=500, verbose_name='回复内容')),
                ('approval_number', models.IntegerField(default=0, verbose_name='获赞数')),
                ('add_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '讨论回复',
                'verbose_name_plural': '讨论回复',
            },
        ),
        migrations.CreateModel(
            name='ShortComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_number', models.IntegerField(db_index=True, default=0, verbose_name='获赞数')),
                ('content', models.CharField(max_length=300, verbose_name='短评内容')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('score', models.IntegerField(default=1, verbose_name='该条短评的评分')),
            ],
            options={
                'verbose_name': '短评',
                'verbose_name_plural': '短评',
            },
        ),
        migrations.CreateModel(
            name='WantEat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.Food', verbose_name='所属美食')),
            ],
            options={
                'verbose_name': '想吃记录',
                'verbose_name_plural': '想吃记录',
            },
        ),
    ]
