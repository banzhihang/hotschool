# Generated by Django 2.2.12 on 2020-07-15 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20200715_1358'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserDynamic',
        ),
    ]