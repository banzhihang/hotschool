# Generated by Django 2.2.12 on 2020-05-18 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('question', '0004_auto_20200518_1505'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotQuestionScoreOneWeeks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(verbose_name='问题的分数')),
            ],
        ),
        migrations.CreateModel(
            name='HotQuestionScoreThreeDays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(verbose_name='问题的分数')),
            ],
        ),
        migrations.CreateModel(
            name='HotQuestionScoreTwentyFouryHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(verbose_name='问题的分数')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='campus',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.Campus', verbose_name='校区'),
        ),
        migrations.AddField(
            model_name='question',
            name='college',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.College', verbose_name='学院'),
        ),
        migrations.AddField(
            model_name='question',
            name='grade',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.Grade', verbose_name='年级'),
        ),
        migrations.AddField(
            model_name='question',
            name='major',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.Major', verbose_name='专业'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='is_anonymity',
            field=models.IntegerField(choices=[(0, '不匿名'), (1, '匿名')], default=0, verbose_name='是否匿名'),
        ),
        migrations.DeleteModel(
            name='SiteCircle',
        ),
        migrations.AddField(
            model_name='hotquestionscoretwentyfouryhours',
            name='question_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question', verbose_name='问题id'),
        ),
        migrations.AddField(
            model_name='hotquestionscorethreedays',
            name='question_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question', verbose_name='问题id'),
        ),
        migrations.AddField(
            model_name='hotquestionscoreoneweeks',
            name='question_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question', verbose_name='问题id'),
        ),
    ]