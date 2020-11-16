import json

from bs4 import BeautifulSoup

from HotSchool.celery import app
from draft.models import AnswerDraft

@app.task
def get_answer_draft_abstract(draft_id):
    """
    获得草稿摘要
    参数:draft_id(草稿id)
    """
    try:
        draft = AnswerDraft.objects.get(pk=int(draft_id))
    except AnswerDraft.DoesNotExist:
        pass
    else:
        html = json.loads(draft.content)
        clean_text = BeautifulSoup(html, "lxml").get_text(strip=True)
        if len(clean_text)>20:
            draft.abstract = clean_text[0:20]+'...'
        else:
            draft.abstract = clean_text[0:20]
        draft.save()
