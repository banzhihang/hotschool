# Generated by Django 2.2.12 on 2020-11-01 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('draft', '0002_fooddraft_flavour'),
        ('user', '0001_initial'),
        ('question', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='fooddraft',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.School', verbose_name='所属学校'),
        ),
        migrations.AddField(
            model_name='fooddraft',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='该美食的作者'),
        ),
        migrations.AddField(
            model_name='answerdraft',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question', verbose_name='所属问题'),
        ),
        migrations.AddField(
            model_name='answerdraft',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='所属的用户'),
        ),
    ]
