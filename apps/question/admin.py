from django.contrib import admin

from question.models import Question, Comment, Revert, Answer

admin.site.register([Comment,Revert,Answer])


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['title']


admin.site.register(Question,QuestionAdmin)