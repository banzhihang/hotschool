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
    # 用户回答,问题,美食
    path('publish', MyPublishView.as_view()),
    # 用户收藏
    path('collect', MyCollectView.as_view()),
    # 我的关注
    #path('myattention', MyAttentionView.as_view()),
    # 用户关注和被关注
    path('attention/<int:user_id>',UserAttention.as_view()),
    # 用户昨日创作者数据
    path('create',UserCreatorDataView.as_view()),
    # 评论详情
    path('comment',CollectCommentInfoView.as_view()),
    path('test',DeleteTestView.as_view())
]
