import redis
from celery import shared_task

from HotSchool.settings import POOL
from food.algorithms import wilson_score_food
from food.models import Food

@shared_task
def calculate_food_score(food_id):
    """
    更新食物的威尔逊得分
    参数:food_id(食物id) 十分钟执行一次
    """
    coon = redis.Redis(connection_pool=POOL)
    food = Food.objects.filter(pk=food_id).values('vote_number','all_score')
    score = wilson_score_food(food[0]['all_score'],food[0]['vote_number'])
    Food.objects.filter(pk=food_id).update(score=score)
    coon.srem('food',food_id)