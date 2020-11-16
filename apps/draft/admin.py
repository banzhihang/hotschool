from django.contrib import admin

from draft.models import AnswerDraft, FoodDraft

admin.site.register([AnswerDraft,FoodDraft])
