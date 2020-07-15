from django.urls import path, re_path

from . import views
from .views import HeadAndNickName

urlpatterns = [
    path('2222/', views.room, name='room'),
    path('3333/', views.room2, name='room'),
    path('userinfo',HeadAndNickName.as_view())
]