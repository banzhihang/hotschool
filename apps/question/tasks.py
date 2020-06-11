from django.db.models import F

from HotSchool.celery import app
from question.models import HotQuestionTwentyFouryHoursOperation, HotQuestionSevenDagsOperation


@app.task
def add_user_browse(question_id, type):
    """将用户的浏览操作添加到热榜操作记录表"""
    # 先去热榜记录表查询该问题是否存在，存在就将相应的字段加一，否则就创建一条记录，并将相应的字段加一
    question = HotQuestionTwentyFouryHoursOperation.objects.filter(question_id=question_id).first()
    if question:
        if type == 0:
            question.sacn_number = question.sacn_number + 1
            question.question.scan_number = question.question.scan_number + 1
        elif type == 1:
            question.answer_number = F('answer_number') + 1
        elif type == 2:
            question.attention_number = F('attention_number') + 1
        elif type == 3:
            question.collect_number = F('collect_number') + 1
        elif type == 4:
            question.comment_number = F('comment_number') + 1

        question.save()

    else:
        if type == 0:
            question = HotQuestionTwentyFouryHoursOperation.objects.create(question_id=question_id)
            question.scan_number = F('scan_number') + 1
        elif type == 1:
            question = HotQuestionTwentyFouryHoursOperation.objects.create(question_id=question_id)
            question.answer_number = F('answer_number') + 1
        elif type == 2:
            question = HotQuestionTwentyFouryHoursOperation.objects.create(question_id=question_id)
            question.attention_number = F('attention_number') + 1
        elif type == 3:
            question = HotQuestionTwentyFouryHoursOperation.objects.create(question_id=question_id)
            question.collect_number = F('collect_number') + 1
        elif type == 4:
            question = HotQuestionTwentyFouryHoursOperation.objects.create(question_id=question_id)
            question.comment_number = F('comment_number') + 1


        question.save()
