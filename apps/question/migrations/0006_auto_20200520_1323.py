# Generated by Django 2.2.12 on 2020-05-20 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0005_auto_20200518_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='score',
            field=models.FloatField(default=0.0, verbose_name='得分'),
        ),
        migrations.AddField(
            model_name='answer',
            name='vote_number',
            field=models.IntegerField(default=0, verbose_name='投票总数'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='approval_number',
            field=models.IntegerField(default=0, verbose_name='赞同数'),
        ),
    ]
