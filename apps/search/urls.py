from django.urls import path,include
from rest_framework import routers

from search.views import FoodSearchView, QuestionSearchView, UserSearchView, SchoolSearchView, FlavourSearchView

# 搜索路由
router = routers.DefaultRouter()
router.register("question", QuestionSearchView, base_name="question_search")
router.register("food",FoodSearchView,base_name='food_search')
router.register("user",UserSearchView,base_name='user_search')
router.register("school",SchoolSearchView,base_name='school_search')
router.register("flavour",FlavourSearchView,base_name='flavour_search')

urlpatterns = [
    path('',include(router.urls))
]