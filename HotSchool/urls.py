"""HotSchool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from HotSchool import settings
from question.views import QuestionView
from recommend.views import RecommendView
from upload.views import UploadTokenView

from user.views import LoginView


urlpatterns = [
    # 管理员
    path('admin/', admin.site.urls),
    # 身份认证
    path('login',LoginView.as_view()),
    # 媒体文件
    re_path(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    # 用户相关
    path('user/', include('user.urls'), name='user'),
    # 问题的回答评论回复相关
    path('question/', include('question.urls'), name='question'),
    # 问题
    path('question',QuestionView.as_view()),
    # 操作相关
    path('operation/', include('operation.urls'), name='operation'),
    # 美食相关
    path('food/', include('food.urls'), name='food'),
    # 聊天相关
    path('chat/', include('communicate.urls'),name='chat'),
    # 搜索
    path('search/', include('search.urls'),name='search'),
    # 上传图片
    path('upload',UploadTokenView.as_view()),
    # 推荐
    path('recommend',RecommendView.as_view()),
    # 草稿箱
    path('draft/',include('draft.urls'),name='draft')
]
