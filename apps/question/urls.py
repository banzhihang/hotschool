from django.urls import path

from .views import *

urlpatterns = [
    # 热榜问题
    path('hot', HotQuestionView.as_view()),
    # 问题详情
    path('question/<int:question_id>', QuestionView.as_view()),
    # 回答详情
    path('answer/<int:answer_id>', AnswerView.as_view()),
    # 评论详情
    path('comment', CommentView.as_view()),
    # 回复详情
    path('revert', RevertView.as_view()),

]
