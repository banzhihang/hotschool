from django.db.models import F

from question.models import *


def approval(user_id, answer_id,type):
    """赞同或者反对,0为赞同，1为反对"""
    if type == 0:
        record = ApprovalAnswerRelation.objects.filter(user=user_id, answer=answer_id,type=0).first()
        answer = Answer.objects.get(pk=answer_id)
        if record:
            record.delete()
            # 赞同数减一，若是反对,则只减少投票总数
            answer.approval_number = F('approval_number') - 1
            # 投票总数加一
            answer.vote_number = F('vote_number') - 1
            msg = '取消成功'
        else:
            record = ApprovalAnswerRelation.objects.create(user=user_id, answer=answer_id,type=0)
            record.save()
            answer.approval_number = F('approval_number') + 1
            answer.vote_number = F('vote_number') + 1
            msg = '赞同成功'
        answer.save()
    else:
        record = ApprovalAnswerRelation.objects.filter(user=user_id, answer=answer_id, type=1).first()
        answer = Answer.objects.get(pk=answer_id)
        if record:
            record.delete()
            answer.vote_number = F('vote_number') - 1
            msg = '取消成功'
        else:
            record = ApprovalAnswerRelation.objects.create(user=user_id, answer=answer_id, type=0)
            record.save()
            answer.vote_number = F('vote_number') + 1
            msg = '赞同成功'
        answer.save()

    return msg