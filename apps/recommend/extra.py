import random
from datetime import datetime,timedelta

import redis

from HotSchool.settings import POOL


def get_answer_id(question_id_list):
    """
    获得推荐回答id
    question_id_list:问题列id表
    返回值:回答id列表和问题id列表
    """
    coon = redis.Redis(connection_pool=POOL)
    answer_results,question_results = [],[]
    for i in question_id_list:
        # 获得该回答前10个回答的id
        answer_id_list = coon.zrange('answer:score:'+str(i),start=0,end=9)
        # 若该问题暂时没有回答,则将该问题添加到另一个list (question_results),否则添加到answer_results
        if answer_id_list:
            # 从10个回答中随机选择一个
            answer_id = random.choice(answer_id_list)
            answer_results.append(int(answer_id))
        else:
            question_results.append(int(i))

    return answer_results,question_results


def mix_answer_and_question(answer_data,question_data):
    """
    混合回答和问题
    参数:answer_data(序列化过的回答数据) question_data(序列化过的问题数据)
    返回值:混合之和的数据
    """
    ans_len,question_len = len(answer_data),len(question_data)
    # 若两者长度都不为0
    if ans_len!=0 and question_len !=0:
        # 若回答长度大于问题
        if ans_len>question_len:
            for i in question_data:
                # 在0到answer_len之间随机选择一个位置将问题数据插入回答数据
                insert_location = random.choice(range(0,ans_len))
                answer_data.insert(insert_location,i)
            return answer_data
        else:
            for i in answer_data:
                insert_location = random.choice(range(0,question_len))
                question_data.insert(insert_location,i)
            return question_data
    else:
        # 谁的长度不为0就返回谁
        if ans_len !=0:
            return answer_data
        else:
            return question_data


def add_user_recommend_record(recommend_list,user_id):
    """
    将推荐过的问题添加到用户的推荐记录set
    :recommend_list(待添加记录)
    :user_id(用户id)
    """
    coon = redis.Redis(connection_pool=POOL)
    # 记录过期时间为2天之后
    expire_time = (datetime.now() + timedelta(days=2)).timestamp()
    record_dict = {}
    for i in recommend_list:
        record_dict[i] = expire_time
    coon.zadd('recom:' + str(user_id),record_dict)
