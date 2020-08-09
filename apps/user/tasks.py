from datetime import datetime,timedelta
import json

import redis
from celery import shared_task
from django.db.models import F

from HotSchool.settings import POOL
from question.models import Answer, Question
from user.models import User, UserDynamic, UserData


@shared_task
def sync_user_dynamic(user_id):
    """
    同步用户的动态(30分钟之后执行)
    参数:user_id(用户id)
    返回值:无
    """
    coon = redis.Redis(connection_pool=POOL)
    # 先判断该用户的动态还在不在redis,不在就直接结束
    is_exist = coon.exists('dynamic:' + str(user_id))
    if is_exist:
        # 去redis 查询这个人的动态，若有,同步此人的动态到数据库
        user_dynamic_list = coon.zrange('dynamic:' + str(user_id), start=0, end=-1, withscores=True)
        if user_dynamic_list:
            coon.delete('dynamic:' + str(user_id))
            # 查询有没有这个人
            try:
                user = User.objects.get(pk=user_id)
            except Exception:
                return
            else:
                dynamics = []
                for i in user_dynamic_list:
                    # 反序列化用户动态的json数据 不含时间戳
                    dynamic = json.loads(i[0])
                    answer_id = dynamic.get('answer')
                    question_id = dynamic.get('question')
                    # 判断该动态是问题相关还是回答相关
                    if answer_id:
                        answer = Answer.objects.filter(pk=answer_id)
                        # 若不存在该id 则抛弃这条动态
                        if answer.exists():
                            dynamic['answer_id'] = int(answer_id)
                            dynamic.pop('answer')
                        else:
                            continue
                    if question_id:
                        question = Question.objects.filter(pk=question_id)
                        if question.exists():
                            dynamic['question_id'] = int(question_id)
                            dynamic.pop('question')
                        else:
                            continue
                    # 将时间戳添加到dynamic字典，创建dynamic对象，最后批量插入数据库
                    dynamic['add_time'] = float(i[1])
                    dynamic['user'] = user
                    j = UserDynamic(**dynamic)
                    dynamics.append(j)
            # 批量插入
            UserDynamic.objects.bulk_create(dynamics)


@shared_task
def sync_user_operation(user_id):
    """
    同步用户的创作者数据
    参数:user_id(用户id)
    返回值:无
    执行时间:每天4点
    """
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d') # 昨天的时间字符串
    coon = redis.Redis(connection_pool=POOL)
    user_data = coon.hmget('ud:'+yesterday+':'+str(user_id),'read','approval','like','collect','comment')
    if user_data:
        # 获取用户在redis中的数据,同步到数据库
        read_number,approval_number,like_number,collect_number,comment_number = int(user_data[0]),int(user_data[1]),int(user_data[2]),int(user_data[3]),int(user_data[4])
        UserData.objects.filter(pk=user_id).update(
            approval_number=F('approval_number')+approval_number,
            like_number=F('like_number')+like_number,
            collect_number=F('collect_number')+collect_number,
            read_number=F('read_number')+read_number,
            comment_number=F('comment_number')+comment_number
        )
