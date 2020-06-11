from django.forms.models import model_to_dict

from question.models import Question, Answer, Comment, Revert
from .models import *


def get_user_info(user_id):
    """获取用户信息"""
    user = User.objects.filter(pk=user_id).only('nick_name', 'head_portrait', 'phone', 'address',
                                                           'desc', 'college',
                                                           'major', 'grade', 'add_time', 'interest').first()
    # 返回一个user对象
    return user


def get_recent_browse(user_id):
    """获取用户最近浏览记录"""
    # 查询最近浏览记录表获得问题id和回答id
    recent_browse_questions = RecentBrowseQuestion.objects.filter(
        user_id=user_id)
    recent_browse_answers = RecentBrowseAnswer.objects.filter(
        user_id=user_id)

    return recent_browse_questions, recent_browse_answers


def get_user_answer(user_id):
    """获取用户回答"""
    # 去问题表查询用户的回答
    my_answers = Answer.objects.filter(user=user_id)

    return my_answers


def get_user_question(user_id):
    """获取用户的问题"""
    my_questions = Question.objects.filter(user=user_id)
    return my_questions


def get_user_comment(user_id):
    """获取用户评论"""
    my_comments = Comment.objects.filter(user=user_id)
    my_reverts = Revert.objects.filter(user=user_id)
    return my_comments, my_reverts


def get_user_collect(user_id):
    """获取用户收藏"""
    user = User.objects.get(pk=user_id)
    # 查询user的question_collect，answer_collect字段( django的多对多)
    my_question_collects = user.question_collect.all()
    my_answer_collects = user.answer_collect.all()

    return my_question_collects, my_answer_collects


def get_user_attention(user_id):
    """获取用户的关注人"""
    user = User.objects.get(pk=user_id)
    my_attention_user = user.attention.all()

    return my_attention_user
