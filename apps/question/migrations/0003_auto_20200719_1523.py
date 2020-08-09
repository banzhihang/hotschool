# Generated by Django 2.2.12 on 2020-07-19 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0002_auto_20200711_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='question.Answer', verbose_name='所属回答'),
        ),
        migrations.AlterField(
            model_name='revert',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='添加时间'),
        ),
        migrations.DeleteModel(
            name='ApprovalAnswerRelation',
        ),
    ]