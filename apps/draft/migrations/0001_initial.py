# Generated by Django 2.2.12 on 2020-08-13 10:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('food', '0020_auto_20200731_2133'),
        ('user', '0015_school_is_campus'),
        ('question', '0012_auto_20200809_2117'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodDraft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20, verbose_name='美食名称')),
                ('image_first', models.URLField(default='', verbose_name='图片url')),
                ('image_second', models.URLField(default='', verbose_name='图片url')),
                ('image_third', models.URLField(default='', verbose_name='图片url')),
                ('image_fourth', models.URLField(default='', verbose_name='图片url')),
                ('image_fifth', models.URLField(default='', verbose_name='图片url')),
                ('address_image', models.URLField(default='', verbose_name='图片url')),
                ('desc', models.CharField(default='', max_length=150, verbose_name='美食简短描述')),
                ('address', models.CharField(default='', max_length=50, verbose_name='美食地址')),
                ('longitude', models.DecimalField(decimal_places=6, default=0, max_digits=40, verbose_name='地点的经度')),
                ('latitude', models.DecimalField(decimal_places=6, default=0, max_digits=40, verbose_name='地点的维度')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('modify_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='修改时间')),
                ('flavour', models.ManyToManyField(to='food.Flavour', verbose_name='美食的味道')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.School', verbose_name='所属学校')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='该美食的作者')),
            ],
            options={
                'verbose_name': '美食草稿',
                'verbose_name_plural': '美食草稿',
            },
        ),
        migrations.CreateModel(
            name='AnswerDraft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_anonymity', models.IntegerField(choices=[(0, '不匿名'), (1, '匿名')], default=0, verbose_name='是否匿名')),
                ('content', models.TextField(default='', max_length=100000, verbose_name='用户回答')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('modify_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='修改时间')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question', verbose_name='所属问题')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='所属的用户')),
            ],
            options={
                'verbose_name': '回答草稿',
                'verbose_name_plural': '回答草稿',
            },
        ),
    ]