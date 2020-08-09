from django.urls import path

from .views import *

urlpatterns = [
    # 赞同
    path('approval',ApprovalView.as_view()),
    # 喜欢
    path('like',LikeView.as_view()),
    # 收藏
    path('collect',CollectView.as_view()),
    # 关注
    path('attention',AttentionView.as_view())
]
