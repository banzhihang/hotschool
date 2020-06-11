# Generated by Django 2.2.12 on 2020-05-28 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0008_auto_20200520_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotQuestionSevenDags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sacn_number', models.IntegerField(default=0, verbose_name='过去7天浏览量')),
                ('answer_number', models.IntegerField(default=0, verbose_name='过去7天回答量')),
                ('attention_number', models.IntegerField(default=0, verbose_name='过去7天关注量')),
                ('collect_number', models.IntegerField(default=0, verbose_name='过去7天收藏量')),
                ('comment_number', models.IntegerField(default=0, verbose_name='过去7天评论量')),
                ('score', models.FloatField(default=0.0, verbose_name='热度值')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question', verbose_name='问题id')),
            ],
        ),
        migrations.CreateModel(
            name='HotQuestionTwentyFouryHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sacn_number', models.IntegerField(default=0, verbose_name='过去24小时浏览量')),
                ('answer_number', models.IntegerField(default=0, verbose_name='过去24小时回答量')),
                ('attention_number', models.IntegerField(default=0, verbose_name='过去24小时关注量')),
                ('collect_number', models.IntegerField(default=0, verbose_name='过去24小时收藏量')),
                ('comment_number', models.IntegerField(default=0, verbose_name='过去24小时评论量')),
                ('score', models.FloatField(default=0.0, verbose_name='热度值')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question', verbose_name='问题id')),
            ],
        ),
        migrations.RemoveField(
            model_name='hotquestion',
            name='question_id',
        ),
        migrations.RemoveField(
            model_name='hotquestionscoreoneweeks',
            name='question_id',
        ),
        migrations.RemoveField(
            model_name='hotquestionscorethreedays',
            name='question_id',
        ),
        migrations.RemoveField(
            model_name='hotquestionscoretwentyfouryhours',
            name='question_id',
        ),
        migrations.DeleteModel(
            name='AllRecentScan',
        ),
        migrations.DeleteModel(
            name='HotQuestion',
        ),
        migrations.DeleteModel(
            name='HotQuestionScoreOneWeeks',
        ),
        migrations.DeleteModel(
            name='HotQuestionScoreThreeDays',
        ),
        migrations.DeleteModel(
            name='HotQuestionScoreTwentyFouryHours',
        ),
    ]
