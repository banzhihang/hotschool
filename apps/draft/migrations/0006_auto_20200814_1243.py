# Generated by Django 2.2.12 on 2020-08-14 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('draft', '0005_auto_20200814_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooddraft',
            name='address',
            field=models.CharField(max_length=50, verbose_name='美食地址'),
        ),
    ]
