from drf_haystack.filters import HaystackHighlightFilter
from drf_haystack.viewsets import HaystackViewSet

from food.models import Food, Flavour
from question.models import Question
from search.filter import SchoolFilter
from search.paginations import UserSearchPagination, FoodSearchPagination, QuestionSearchPagination, \
    SchoolSearchPagination, FlavourSearchPagination
from search.serializers import QuestionSearchSerializer, FoodSearchSerializer, UserSearchSerializer, \
    SchoolSearchSerializer, FlavourSearchSerializer
from user.models import User, School


class QuestionSearchView(HaystackViewSet):
    """问题搜索视图"""
    index_models = [Question]
    serializer_class = QuestionSearchSerializer
    pagination_class = QuestionSearchPagination
    filter_backends = [HaystackHighlightFilter]

class FoodSearchView(HaystackViewSet):
    """美食搜索视图"""
    index_models = [Food]
    serializer_class = FoodSearchSerializer
    filter_backends = [HaystackHighlightFilter]
    pagination_class = FoodSearchPagination


class UserSearchView(HaystackViewSet):
    """用户搜索视图"""
    index_models = [User]
    serializer_class = UserSearchSerializer
    # 分页器
    pagination_class = UserSearchPagination
    filter_backends = [HaystackHighlightFilter]


class SchoolSearchView(HaystackViewSet):
    """学校搜索视图"""
    index_models = [School]
    # 序列化器
    serializer_class = SchoolSearchSerializer
    # 过滤器
    filter_backends = [SchoolFilter,HaystackHighlightFilter]
    pagination_class = SchoolSearchPagination


class FlavourSearchView(HaystackViewSet):
    """口味搜索序列化器"""
    index_models = [Flavour]
    serializer_class = FlavourSearchSerializer
    # 分页器
    pagination_class = FlavourSearchPagination
    # 高亮
    filter_backends = [HaystackHighlightFilter]