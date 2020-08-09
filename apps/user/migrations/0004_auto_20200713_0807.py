# Generated by Django 2.2.12 on 2020-07-13 00:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20200713_0805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='id',
        ),
        migrations.AlterField(
            model_name='userdata',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]