# Generated by Django 2.2.12 on 2020-11-01 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='', max_length=100000, verbose_name='用户回答')),
                ('abstract', models.CharField(default='', max_length=100, verbose_name='回答摘要')),
                ('first_image', models.URLField(max_length=300, null=True, verbose_name='回答第一张图片')),
                ('is_anonymity', models.IntegerField(choices=[(0, '不匿名'), (1, '匿名')], default=0, verbose_name='是否匿名')),
                ('vote_number', models.IntegerField(default=0, verbose_name='投票总数')),
                ('approval_number', models.IntegerField(default=0, verbose_name='赞同数')),
                ('comment_number', models.IntegerField(default=0, verbose_name='评论数')),
                ('score', models.FloatField(default=0.0, verbose_name='得分')),
                ('like_number', models.IntegerField(default=0, verbose_name='喜欢数')),
                ('collect_number', models.IntegerField(default=0, verbose_name='收藏数')),
                ('add_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='添加时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '回答',
                'verbose_name_plural': '回答',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_anonymity', models.IntegerField(choices=[(0, '不匿名'), (1, '匿名')], default=0, verbose_name='是否匿名')),
                ('content', models.TextField(default='', max_length=1000, verbose_name='用户评论')),
                ('revert_number', models.IntegerField(default=0, verbose_name='回复数数')),
                ('approval_number', models.IntegerField(db_index=True, default=0, verbose_name='获赞数')),
                ('add_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=100, verbose_name='问题标题')),
                ('abstract', models.CharField(default='', max_length=100, verbose_name='问题摘要')),
                ('content', models.TextField(default='', max_length=200, verbose_name='问题内容')),
                ('attention_number', models.IntegerField(default=0, verbose_name='关注人数')),
                ('scan_number', models.IntegerField(default=0, verbose_name='浏览总量')),
                ('answer_number', models.IntegerField(default=0, verbose_name='回答总数')),
                ('is_anonymity', models.IntegerField(choices=[(0, '不匿名'), (1, '匿名')], default=0, verbose_name='是否匿名')),
                ('add_time', models.DateField(auto_now_add=True, verbose_name='问题发布时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '问题',
                'verbose_name_plural': '问题',
            },
        ),
        migrations.CreateModel(
            name='Revert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_user_anonymity', models.IntegerField(choices=[(0, '不匿名'), (1, '匿名')], default=0, verbose_name='用户是否匿名')),
                ('is_target_user_anonymity', models.IntegerField(choices=[(0, '不匿名'), (1, '匿名')], default=0, verbose_name='目标用户是否匿名')),
                ('content', models.CharField(default='', max_length=100, verbose_name='回复内容')),
                ('approval_number', models.IntegerField(default=0, verbose_name='获赞数')),
                ('add_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='添加时间')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Comment', verbose_name='所属的评论')),
            ],
            options={
                'verbose_name': '回复',
                'verbose_name_plural': '回复',
            },
        ),
    ]
