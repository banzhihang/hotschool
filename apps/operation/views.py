import json

from django.http import HttpResponse
from django.views.generic.base import View

from .logics import *


class ApprovalView(View):
    """
    赞同或者反对
    参数:user_id,answer_id
    """

    def get(self, request):
        user_id = request.GET.get('user_id', '')
        answer_id = request.GET.get('answer_id', '')
        type = request.GET.get('type', '')

        message = approval(user_id, answer_id, type)

        data = {
            'message': message
        }

        return HttpResponse(json.dumps(data, cls=JsonToDatetime))
