from django.forms.models import model_to_dict

from user.models import Campus, College, Grade
from .models import *


def get_hot_question(campus, college, grade, time_slot_type):
    """获取热门内容"""
    def get_questions_list(questions_id_set):
        """将查询到的问题id集和转换成问题列表"""
        question_set = []
        for i in questions_id_set:
            # 得到id去问题表查询详细内容
            question = Question.objects.get(pk=i.question_id_id)
            question = model_to_dict(question)
            question_set.append(question)
        return question_set

    # 判断时间点(0为24小时,1为一周)
    if time_slot_type == 0:
        # 判断地点圈子(只有校区才能选择时间,其他地点圈子不能选择时间(只能为24小时))
        if campus:
            # 去campus表查询 campus的id
            campus = Campus.objects.filter(name=campus).only('id').first().id
            # 获得campus的id后去热门问题表查询问题，并筛选(已排序)
            questions_set = HotQuestionTwentyFouryHours.objects.filter(question_id__campus=campus).only(
                'question_id').order_by('-score')
            questions = get_questions_list(questions_set)
        elif college:
            college = College.objects.filter(name=college).only('id').first().id
            questions_set = HotQuestionTwentyFouryHours.objects.filter(question_id__college=college).only(
                'question_id').order_by('-score')
            questions = get_questions_list(questions_set)

    elif time_slot_type == 1:
        campus = Campus.objects.filter(name=campus).only('id').first().id
        questions_set = HotQuestionSevenDags.objects.filter(question_id__campus=campus).only(
            'question_id').order_by('-score')
        questions = get_questions_list(questions_set)

    return questions



def get_revert(comment_id):
    """
    获取用户回复
    参数：comment_id
    返回值：回复列表
    """
    reverts = Revert.objects.filter(comment=comment_id).order_by('modify_time')
    reverts = [model_to_dict(revert) for revert in reverts]

    return reverts
