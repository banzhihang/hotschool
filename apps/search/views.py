from drf_haystack.viewsets import HaystackViewSet

from food.models import Food, Flavour
from puclic import LooseAuthtication
from question.models import Question
from search.filter import SchoolFilter, FoodEmptyFilter, AllEmptyFilter
from search.paginations import UserSearchPagination, FoodSearchPagination, QuestionSearchPagination, \
    SchoolSearchPagination, FlavourSearchPagination
from search.serializers import QuestionSearchSerializer, FoodSearchSerializer, UserSearchSerializer, \
    SchoolSearchSerializer, FlavourSearchSerializer
from user.models import User, School


class QuestionSearchView(HaystackViewSet):
    """问题搜索视图"""
    index_models = [Question]
    serializer_class = QuestionSearchSerializer
    filter_backends = [AllEmptyFilter]
    pagination_class = QuestionSearchPagination


class FoodSearchView(HaystackViewSet):
    """美食搜索视图"""

    index_models = [Food]
    serializer_class = FoodSearchSerializer
    filter_backends = [FoodEmptyFilter]
    pagination_class = FoodSearchPagination


class UserSearchView(HaystackViewSet):
    """用户搜索视图"""

    # 用户认证
    authentication_classes = [LooseAuthtication, ]
    index_models = [User]
    serializer_class = UserSearchSerializer
    # 分页器
    pagination_class = UserSearchPagination
    filter_backends = [AllEmptyFilter]


class SchoolSearchView(HaystackViewSet):
    """学校搜索视图"""

    index_models = [School]
    # 序列化器
    serializer_class = SchoolSearchSerializer
    # 过滤器
    filter_backends = [SchoolFilter]
    pagination_class = SchoolSearchPagination


class FlavourSearchView(HaystackViewSet):
    """口味搜索序列化器"""

    index_models = [Flavour]
    serializer_class = FlavourSearchSerializer
    filter_backends = [AllEmptyFilter]
    # 分页器
    pagination_class = FlavourSearchPagination
