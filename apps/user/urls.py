from django.urls import path, include

from .views import *

urlpatterns = [
    # 用户信息
    path('userinfo', UserInfoView.as_view()),
    # 用户信息展示
    path('infoshow/<int:user_id>',UserInfoShowView.as_view()),
    # 用户动态
    path('dynamic/<int:user_id>',UserDynamicView.as_view()),
    # 用户最近浏览记录
    path('recentbrowse', RecentBrowseView.as_view()),
    # 用户回答,评论，回复
    path('answer', MyAnswerView.as_view()),
    # 用户问题
    path('question', MyQuestionView.as_view()),
    # 用户收藏
    path('collect', MyCollectView.as_view()),
    # 我的关注
    path('myattention', MyAttentionView.as_view()),
    # 用户关注和被关注
    path('attention/<int:user_id>',UserAttention.as_view())

]
