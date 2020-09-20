import time
import datetime
import re

import redis
from bs4 import BeautifulSoup

from HotSchool.settings import POOL
from question.models import Question, Answer
from question.tasks import calculate_question_and_sync
from user.tasks import sync_user_operation


def add_question_operation_data(operation, question_id, type=None):
    """
    为问题添加操作数据
    参数:1.operation(操作类型 'scan':增加浏览量 'answer':增加回答量,
    'approval':(增加赞同量),'attention':(增加关注量(问题的关注量)), 'comment':(增加评论量)),'collect':收藏增量
        2.coon:redis连接
        3.question_id:问题id
        4.type 若operation为attention 则type必须存在,若为reduce则为减少,若type不为reduce,则正常操作
    """
    question_id = int(question_id)
    coon = redis.Redis(connection_pool=POOL)
    today = time.strftime('%Y%m%d')
    # 添加数据之前先判断该问题今天是不是第一次浏览
    if operation == 'scan':
        question_exists = coon.exists('qd:' + str(question_id) + ':' + today)
        # 若redis没有该键,则说明这个问题今天是第一次浏览, 添加各种数据，同时设置过期时间
        if not question_exists:
            question_school_id_set = Question.objects.filter(pk=question_id).values_list('school_id')
            school_id = question_school_id_set[0][0]
            coon.hmset('qd:' + str(question_id) + ':' + today,
                       {'scan': 0, 'answer': 0, 'approval': 0, 'attention': 0, 'comment': 0, 'collect': 0,
                        'school': school_id})

            # 添加一个定时任务,第二天半夜一点计算热度值,并同步数据到数据库
            tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
            execute_time = datetime.datetime.utcfromtimestamp(datetime.datetime(
                tomorrow.year, tomorrow.month, tomorrow.day, 1, 0, 0).timestamp())
            calculate_question_and_sync.apply_async(args=[question_id], eta=execute_time)

    elif operation == 'attention':
        if type == 'reduce':
            coon.hincrby('qd:' + str(question_id) + ':' + today, 'attention', -1)
            return
    # 将相应的数据增加1
    coon.hincrby('qd:' + str(question_id) + ':' + today, operation, 1)


def add_user_operation_data(operation, target_user_id, type=None, user_id=None, answer_id=None):
    """
     添加用户创作数据
    :param operation: 操作类型 'read'阅读，'approval'赞同  'like'喜欢  'collect'收藏,'attention'关注
    :param target_user_id: 该回答的作者的id
    :param type:该操作是增加还是减少
    :param user_id: 浏览该回答的用户id
    :param answer_id: 该回答的的id
    """
    today, now_timestamp = time.strftime('%Y%m%d'), time.time()  # 现在时间字符串和时间戳
    coon = redis.Redis(connection_pool=POOL)
    # 若operation 为read 先检查该键是否存在，不存在就先创建，并设置过期时间
    if operation == 'read' or operation == 'attention':
        user_data_exists = coon.exists('ud:' + today + ':' + str(target_user_id))
        if not user_data_exists:
            coon.hmset('ud:' + today + ':' + str(target_user_id), {
                'read': 0, 'approval': 0, 'like': 0, 'collect': 0, 'comment': 0, 'attention': 0})
            coon.hincrby('ud:' + today + ':' + str(target_user_id), operation, 1)
            # redis 用户的创作数据过期时间为第后天0点1分
            tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
            after_tomorrow = datetime.datetime.now() + datetime.timedelta(days=2)  # 后天
            expireat_time = datetime.datetime(after_tomorrow.year, after_tomorrow.month, after_tomorrow.day, 0, 1, 0)
            coon.expireat('ud:' + today + ':' + str(target_user_id), expireat_time)
            # 明天4点将该用户的创作者数据同步到数据库
            execute_time = datetime.datetime.utcfromtimestamp(datetime.datetime(
                tomorrow.year, tomorrow.month, tomorrow.day, 4, 0, 0).timestamp())
            sync_user_operation.apply_async(args=[target_user_id], eta=execute_time)

            if operation == 'read':
                user_recentbrowse_length = coon.zcard('recentbrowse:' + str(user_id))
                if user_recentbrowse_length >= 1000:
                    coon.zremrangebyrank('recentbrowse:' + str(user_id), min=0, max=500)
                coon.zrem('recentbrowse:' + str(user_id), str(answer_id))
                coon.zadd('recentbrowse:' + str(user_id), {str(answer_id): now_timestamp})

        else:
            # 若操作为attention,则要判断是增加还是减少
            if operation == 'attention':
                if type == 'reduce':
                    number = coon.hget('ud:' + today + ':' + str(target_user_id), operation)
                    if number != 0:
                        coon.hincrby('ud:' + today + ':' + str(target_user_id), operation, -1)
                else:
                    coon.hincrby('ud:' + today + ':' + str(target_user_id), operation, 1)
            else:
                # 相应作者的对应数据加一
                coon.hincrby('ud:' + today + ':' + str(target_user_id), operation, 1)
                # 检查该作者的浏览记录zset长度(若不存在该键，则返回0)，若大于1000,就删除最后500个。添加之前先删除之前该回答的浏览记录，相当于更新时间戳
                user_recentbrowse_length = coon.zcard('recentbrowse:' + str(user_id))
                if user_recentbrowse_length >= 1000:
                    coon.zremrangebyrank('recentbrowse:' + str(user_id), min=0, max=500)
                coon.zrem('recentbrowse:' + str(user_id), str(answer_id))
                coon.zadd('recentbrowse:' + str(user_id), {str(answer_id): now_timestamp})

    else:
        if type == 'add':
            # 相应作者的创作数据加一
            coon.hincrby('ud:' + today + ':' + str(target_user_id), operation, 1)
        elif type == 'reduce':
            # 减一
            number = coon.hget('ud:' + today + ':' + str(target_user_id), operation)
            if number != 0:
                coon.hincrby('ud:' + today + ':' + str(target_user_id), operation, -1)


def get_hot_question_image(question_model):
    """
    获得热榜问题的配图
    参数:question_id(问题id)
    返回值:图片url
    """
    coon = redis.Redis(connection_pool=POOL)
    # 最多检查前50个回答,若前50个回答都没有配图,就不再检查
    for i in range(5):
        answer_id_list = coon.zrevrange('answer:score:' + str(question_model.pk), start=i * 10, end=(i + 1) * 10)
        # 若redis返回的回答列表为空,就说明没有回答了,就返回空
        if answer_id_list:
            answer_set = Answer.objects.filter(id__in=answer_id_list).values_list('first_image')
        else:
            return None
        # 检查回答的first_image是否为None,若不是,说明存在图片,直接返回
        for image in answer_set:
            if image[0]:
                return image[0]
        # 若回答id列表小于10,说明此次redis返回的回答id已到达最末尾几个回答,直接返回
        if len(answer_id_list) <10:
            return None





