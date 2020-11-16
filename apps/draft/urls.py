from django.urls import path

from .views import *

urlpatterns = [
    # 我的草稿
    path('mydraft',MyDraftView.as_view()),
    # 回答草稿
    path('answer', AnswerDraftView.as_view()),
    # 美食草稿
    path('food',FoodDraftView.as_view())
]