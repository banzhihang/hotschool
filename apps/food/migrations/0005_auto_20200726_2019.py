# Generated by Django 2.2.12 on 2020-07-26 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0004_auto_20200726_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='shortcomment',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='添加时间'),
        ),
    ]
