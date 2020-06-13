
from question.models import Question, Answer, Comment, Revert
from .models import *

def delete_recent_browse(request,answter_record_list,question_record_list):
    """删除用户浏览记录"""
    if answter_record_list:
        try:
            RecentBrowseAnswer.objects.filter(answer_id__in=answter_record_list,
                                              user_id=request.user.id).delete()
            state1 = 'ok'
        except Exception:
            state1 = 'fail'
    if question_record_list:
        try:
            RecentBrowseQuestion.objects.filter(question_id__in=question_record_list,
                                                user_id=request.user.id).delete()
            state2 = 'ok'
        except Exception:
            state2 = 'fail'

    return state1,state2










