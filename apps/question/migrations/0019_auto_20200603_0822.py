# Generated by Django 2.2.12 on 2020-06-03 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0018_answer_comment_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='interest_circle',
            field=models.ManyToManyField(to='user.Interest', verbose_name='问题的兴趣圈子'),
        ),
    ]