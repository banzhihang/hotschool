# Generated by Django 2.2.12 on 2020-07-26 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food',
            old_name='look_number',
            new_name='eat_number',
        ),
    ]
