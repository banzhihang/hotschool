import json
import time

import redis
from datetime import datetime, timedelta

from HotSchool.settings import POOL
from question.models import Answer
from user.models import UserDynamic
from user.tasks import sync_user_dynamic
from .tasks import calculate_answer_score


def load_answer_operation(answer_id):
    """
    加载回答数据,同步redis,并设置刷回数据库的定时任务
    :param answer_id: 回答id
    return 该回答的作者id和该回答所属的问题的id
    """
    answer_id = int(answer_id)
    coon = redis.Redis(connection_pool=POOL)
    # 检查该问题的数据存不存在redis中,不存在就先去数据库获取,存在就直接修改数据
    answer_data_exists = coon.exists('ad:' + str(answer_id))

    if not answer_data_exists:
        # 去数据库获得该回答的数据,并将该数据同步到redis,同时将该回答id添加到修改过数据的回答的set
        answer = Answer.objects.filter(pk=answer_id).values('approval_number', 'vote_number', 'collect_number',
                                                              'user_id', 'question_id')
        # 若answer为空,则返回None
        if answer:
            answer = answer[0]
        else:
            return None,None
        coon.hmset('ad:' + str(answer_id),
                   {'approval': answer['approval_number'], 'vote': answer['vote_number'], 'collect': answer['collect_number'],
                    'user': answer['user_id'], 'question': answer['question_id']})

        #  定时15分钟后同步该回答的数据到数据库
        execute_time = datetime.fromtimestamp(
            (datetime.now() + timedelta(minutes=15)).timestamp())
        calculate_answer_score.apply_async(args=[answer['question_id'], answer_id], eta=execute_time)

    # 获取回答对应的作者id和问题id,并返回
    answer_user_and_question = coon.hmget('ad:' + str(answer_id), 'user', 'question')
    user, question = answer_user_and_question[0], answer_user_and_question[1]

    return user,question

def add_user_dynamic(operation,type,user_id,answer_id=None,question_id=None):
    """
    添加用户动态(question和answer为二选一参数)
    :param operation:操作类型,'add':创建动态,'delete':删除动态
    :param type: 动态类型(0赞同回答,1收藏回答,2回答问题,3关注问题,4提出问题)
    :param user_id:创建或删除动态的用户
    :param answer: 动态相关回答
    :param question: 动态相关问题
    :return:
    """
    if answer_id:
        user_id,answer_id = int(user_id),int(answer_id)
    elif question_id:
        user_id,question_id = int(user_id),int(question_id)
    else:
        return
    coon = redis.Redis(connection_pool=POOL)
    # 现在的时间戳
    now_timestamp = time.time()
    # 查询该用户的id在不在动态记录set,不存在说明最近半小时redis中没有用户的动态,就创建一个定时任务,半小时后同步用户的动态到数据库
    is_exist = coon.exists('dynamic:' + str(user_id))
    if not is_exist:
        execute_time = datetime.fromtimestamp((datetime.now() + timedelta(minutes=30)).timestamp())
        sync_user_dynamic.apply_async(args=[user_id],eta=execute_time)
    # 若operation为add,则为增加动态,若operation为delete则为删除动态
    if operation == 'add':
        if answer_id:
            # 若type in [0,1,2],则为回答相关
            if type in [0,1,2]:
                # 创建动态,添加到redis中,score为当前时间戳
                dynamic = {'type':type,'answer':answer_id,'user':user_id}
                coon.zadd('dynamic:'+str(user_id),{json.dumps(dynamic,ensure_ascii=False):now_timestamp})
        elif question_id:
            # 若type in [0,1,2],则为问题相关
            if type in [3,4]:
                dynamic = {'type':type,'question':question_id,'user':user_id}
                coon.zadd('dynamic:' + str(user_id), {json.dumps(dynamic, ensure_ascii=False): now_timestamp})

    elif operation == 'delete':
        if answer_id:
            if type in [0,1,2]:
                dynamic = {'type':type,'answer':answer_id,'user':user_id}
                # 检查该条动态存不存在redis中,存在就直接在redis中删除,否则去数据库中删除
                dynamic_exist = coon.zrank('dynamic:'+str(user_id),json.dumps(dynamic,ensure_ascii=False))
                # 若查不到该动态,直接返回
                if dynamic_exist is None:
                    try:
                        UserDynamic.objects.get(user=user_id, type=type, question=question_id).delete()
                    except Exception:
                        return
                else:
                    coon.zrem('dynamic:'+str(user_id),json.dumps(dynamic,ensure_ascii=False))

        elif question_id:
            if type in [3,4]:
                dynamic = {'type': type, 'question': question_id, 'user': user_id}
                dynamic_exist = coon.zrank('dynamic:' + str(user_id), json.dumps(dynamic, ensure_ascii=False))
                if dynamic_exist is None:
                    try:
                        UserDynamic.objects.get(user=user_id, type=type, question=question_id).delete()
                    except Exception:
                        return
                else:
                    coon.zrem('dynamic:' + str(user_id), json.dumps(dynamic, ensure_ascii=False))


