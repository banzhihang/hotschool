# Generated by Django 2.2.12 on 2020-09-08 04:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_school_is_campus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='interest',
        ),
    ]