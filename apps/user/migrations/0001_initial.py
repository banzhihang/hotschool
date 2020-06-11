# Generated by Django 2.2.12 on 2020-05-17 08:38

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('question', '0001_initial'),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('we_chat_openid', models.CharField(default='', max_length=100, verbose_name='微信openid')),
                ('we_chat_unionid', models.CharField(default='', max_length=100, verbose_name='微信unionid')),
                ('phone', models.CharField(db_index=True, default='', max_length=12, verbose_name='手机号码')),
                ('nick_name', models.CharField(default='', max_length=50, verbose_name='昵称')),
                ('age', models.IntegerField(default='', verbose_name='年龄')),
                ('address', models.CharField(default='', max_length=50, verbose_name='所在地')),
                ('desc', models.CharField(default='', max_length=50, verbose_name='自我描述')),
                ('add_time', models.DateField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20, verbose_name='校区名')),
                ('desc', models.CharField(default='', max_length=100, verbose_name='描述')),
                ('school', models.CharField(default='', max_length=30, verbose_name='所属学校')),
            ],
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20, verbose_name='学院名')),
                ('desc', models.CharField(default='', max_length=100, verbose_name='描述')),
                ('campus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Campus')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField(verbose_name='年级')),
                ('desc', models.CharField(max_length=50, verbose_name='描述')),
            ],
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20, verbose_name='兴趣名称')),
                ('desc', models.CharField(default='', max_length=50, verbose_name='描述')),
            ],
        ),
        migrations.CreateModel(
            name='RecentBrowse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('browse_id', models.IntegerField(verbose_name='最近浏览的帖子或回答id')),
                ('type', models.IntegerField(choices=[(0, '问题'), (1, '回答')])),
                ('add_time', models.DateTimeField(auto_now=True, verbose_name='浏览时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MyQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question', verbose_name='问题id')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MyComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Comment', verbose_name='评论id')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MyCollect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collect_id', models.IntegerField(verbose_name='收藏的帖子问题或者回答')),
                ('type', models.IntegerField(choices=[(0, '问题'), (1, '回答')])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MyAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Answer', verbose_name='回答id')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, verbose_name='专业名')),
                ('desc', models.CharField(default='', max_length=100, verbose_name='描述')),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.College')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='campus',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='user.Campus', verbose_name='校区'),
        ),
        migrations.AddField(
            model_name='user',
            name='college',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='user.College', verbose_name='学院'),
        ),
        migrations.AddField(
            model_name='user',
            name='grade',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='user.Grade', verbose_name='年级'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='interest',
            field=models.ManyToManyField(to='user.Interest', verbose_name='用户兴趣'),
        ),
        migrations.AddField(
            model_name='user',
            name='major',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='user.Major', verbose_name='专业'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]