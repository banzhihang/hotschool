# Generated by Django 2.2.12 on 2020-07-26 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0003_auto_20200726_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='latitude',
            field=models.DecimalField(decimal_places=30, default=0, max_digits=40, verbose_name='地点的维度'),
        ),
        migrations.AlterField(
            model_name='food',
            name='longitude',
            field=models.DecimalField(decimal_places=30, default=0, max_digits=40, verbose_name='地点的经度'),
        ),
    ]
