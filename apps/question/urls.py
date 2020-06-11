from django.urls import path, include

from .views import *

urlpatterns = [
    # 热榜问题
    path('hot/', HotQuestionView.as_view()),
    # 问题详情
    path('questioninfo/<int:question_id>/', AQuestionView.as_view()),
    # 评论详情
    path('comments/', CommentView.as_view()),
    # 回答详情
    path('reverts/', RevertView.as_view()),

]
