from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('2222/', views.room, name='room'),
    path('3333/', views.room2, name='room')
]