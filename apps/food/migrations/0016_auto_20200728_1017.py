# Generated by Django 2.2.12 on 2020-07-28 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0015_auto_20200728_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodcomment',
            name='approval_number',
            field=models.IntegerField(default=0, verbose_name='获赞数'),
        ),
        migrations.AlterField(
            model_name='foodcomment',
            name='revert_number',
            field=models.IntegerField(db_index=True, default=0, verbose_name='回复数'),
        ),
    ]
