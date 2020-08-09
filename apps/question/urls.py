from django.urls import path

from .views import *

urlpatterns = [
    # 热榜
    path('hot', HotQuestionView.as_view()),
    # 回答
    path('answer', AnswerView.as_view()),
    # 评论
    path('comment', CommentView.as_view()),
    # 回复
    path('revert', RevertView.as_view()),

]
