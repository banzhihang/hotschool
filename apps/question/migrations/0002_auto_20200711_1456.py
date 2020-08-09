# Generated by Django 2.2.12 on 2020-07-11 06:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='revert',
            name='target_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revert_target_user', to=settings.AUTH_USER_MODEL, verbose_name='被回复的人'),
        ),
        migrations.AddField(
            model_name='revert',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revert_comment_user', to=settings.AUTH_USER_MODEL, verbose_name='所属的用户'),
        ),
        migrations.AddField(
            model_name='question',
            name='interest_circle',
            field=models.ManyToManyField(to='user.Interest', verbose_name='问题的兴趣圈子'),
        ),
        migrations.AddField(
            model_name='question',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.School', verbose_name='所属学校'),
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='所属的用户'),
        ),
        migrations.AddField(
            model_name='comment',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Answer', verbose_name='所属回答'),
        ),
        migrations.AddField(
            model_name='comment',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question', verbose_name='所属问题'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='所属用户'),
        ),
        migrations.AddField(
            model_name='approvalanswerrelation',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Answer', verbose_name='回答'),
        ),
        migrations.AddField(
            model_name='approvalanswerrelation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question', verbose_name='所属问题'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='所属用户'),
        ),
    ]