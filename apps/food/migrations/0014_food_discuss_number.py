# Generated by Django 2.2.12 on 2020-07-28 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0013_food_short_comment_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='discuss_number',
            field=models.IntegerField(default=0, verbose_name='讨论数'),
        ),
    ]
