# Generated by Django 2.2.12 on 2020-05-28 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0010_auto_20200528_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotquestionsevendagsoperation',
            name='answer_number',
            field=models.IntegerField(default=1, verbose_name='过去7天回答量'),
        ),
        migrations.AlterField(
            model_name='hotquestionsevendagsoperation',
            name='attention_number',
            field=models.IntegerField(default=1, verbose_name='过去7天关注量'),
        ),
        migrations.AlterField(
            model_name='hotquestionsevendagsoperation',
            name='collect_number',
            field=models.IntegerField(default=1, verbose_name='过去7天收藏量'),
        ),
        migrations.AlterField(
            model_name='hotquestionsevendagsoperation',
            name='comment_number',
            field=models.IntegerField(default=1, verbose_name='过去7天评论量'),
        ),
        migrations.AlterField(
            model_name='hotquestionsevendagsoperation',
            name='sacn_number',
            field=models.IntegerField(default=1, verbose_name='过去7天浏览量'),
        ),
        migrations.AlterField(
            model_name='hotquestiontwentyfouryhoursoperation',
            name='answer_number',
            field=models.IntegerField(default=1, verbose_name='过去24小时回答量'),
        ),
        migrations.AlterField(
            model_name='hotquestiontwentyfouryhoursoperation',
            name='attention_number',
            field=models.IntegerField(default=1, verbose_name='过去24小时关注量'),
        ),
        migrations.AlterField(
            model_name='hotquestiontwentyfouryhoursoperation',
            name='collect_number',
            field=models.IntegerField(default=1, verbose_name='过去24小时收藏量'),
        ),
        migrations.AlterField(
            model_name='hotquestiontwentyfouryhoursoperation',
            name='comment_number',
            field=models.IntegerField(default=1, verbose_name='过去24小时评论量'),
        ),
        migrations.AlterField(
            model_name='hotquestiontwentyfouryhoursoperation',
            name='sacn_number',
            field=models.IntegerField(default=1, verbose_name='过去24小时浏览量'),
        ),
    ]
