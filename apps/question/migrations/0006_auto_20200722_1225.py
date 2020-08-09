# Generated by Django 2.2.12 on 2020-07-22 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0005_auto_20200722_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='revert_number',
            field=models.IntegerField(default=0, verbose_name='回复数数'),
        ),
        migrations.AlterField(
            model_name='revert',
            name='is_target_user_anonymity',
            field=models.IntegerField(choices=[(0, '不匿名'), (1, '匿名')], default=0, verbose_name='目标用户是否匿名'),
        ),
    ]