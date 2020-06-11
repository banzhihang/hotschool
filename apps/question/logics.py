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


def get_question_info(question_id, type):
    """获取问题详情"""
    # 去Question表查询问题
    question = Question.objects.get(pk=question_id)

    # 用question_id 和type(0为默认排序,1为按时间排序)去Answer表查询回答，并根据score或者添加时间 排序
    if type == 0:
        answers = Answer.objects.filter(question=question_id).order_by('-score')
    else:
        answers = Answer.objects.filter(question=question_id).order_by('-add_time')

    return question, answers


def get_comment(answer_id, comment_type, question_id):
    """获取评论
    参数：问题id或者回答id,comment_id
    返回值：评论列表
    """
    comment_type = int(comment_type)
    # comment_type为0，代表为回答评论,为1,代表为问题评论
    if comment_type == 0:
        comments = Comment.objects.filter(answer=answer_id, type=comment_type).order_by('modify_time')
        comments = [model_to_dict(comment) for comment in comments]
    else:
        comments = Comment.objects.filter(question=question_id, type=comment_type).order_by('modify_time')
        comments = [model_to_dict(comment) for comment in comments]

    return comments


def get_revert(comment_id):
    """
    获取用户回复
    参数：comment_id
    返回值：回复列表
    """
    reverts = Revert.objects.filter(comment=comment_id).order_by('modify_time')
    reverts = [model_to_dict(revert) for revert in reverts]

    return reverts
