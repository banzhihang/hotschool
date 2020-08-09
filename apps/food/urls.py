from django.urls import path

from .views import *

urlpatterns =[
    # 美食排名
    path('rank',FoodView.as_view()),
    # 美食详情
    path('info',FoodInfoView.as_view()),
    # 美食短评
    path('shortcomment',ShortCommentView.as_view()),
    # 美食讨论排行
    path('discuss/rank',DiscussRankView.as_view()),
    # 讨论详情
    path('discuss/info',DiscussInfoView.as_view()),
    # 讨论评论
    path('discuss/comment',FoodCommentView.as_view()),
    # 讨论回复
    path('discuss/revert',FoodRevertView.as_view())
]