import base64
import re
import time
from datetime import datetime,timedelta
import redis
from bs4 import BeautifulSoup

from django.db.models import F

from HotSchool.celery import app
from HotSchool.settings import domain_name, POOL
from communicate.extra import notification_user
from food.models import Discuss, FoodComment
from question.algorithms import calculate_question_hot_score
from question.models import Answer, Comment, Question


@app.task
def push_to_user(from_user, to_user, type, instance=None,content=None):
    """
    通知用户的异步任务
    from_user:引发推送的用户(一个对象)
    to_user:推送的目标用户
    instance:引发推送的实列(例如评论,回复等)
    :type:通知类型
    执行时间:发生动态之后
    """
    to_user,type = int(to_user),int(type)
    # 现在的时间戳
    now_time = time.time()
    # 回复人的昵称
    user_nick_name = from_user.nick_name
    # 回复人的头像url
    user_head_portrait = domain_name + from_user.head_portrait.url
    if type == 3:  # 回复
        # 该回复所属的回答,和评论
        answer_set = Answer.objects.filter(comment__revert=instance).values('id', 'question__title','question_id')
        comment_set = Comment.objects.filter(revert=instance).values('id')
        # 封装进字典
        push_data = {'user': from_user.pk, 'user_nick_name': user_nick_name, 'user_head_portrait': user_head_portrait,
                     'answer': answer_set[0]['id'], 'question_title': answer_set[0]['question__title'],
                     'comment': comment_set[0]['id'], 'content': instance.content}
        data = {'from_user': -1, 'message': push_data, 'time': now_time, 'type': 3}
        # 调用真正的推送函数(to_user为接收者id)
        notification_user(to_user, data)

    elif type == 2:  # 关注
        push_data = {'user': from_user.pk, 'user_nick_name': user_nick_name, 'user_head_portrait': user_head_portrait}
        data = {'from_user': -1, 'message': push_data, 'time': now_time, 'type': 2}
        notification_user(to_user, data)

    elif type == 1:  # 评论
        answer_set = Answer.objects.filter(comment=instance).values('id','question_id','question__title')
        push_data = {'user': from_user.pk, 'user_nick_name': user_nick_name, 'user_head_portrait': user_head_portrait,
                     'question_title': answer_set[0]['question__title'], 'question': answer_set[0]['question_id'],
                     'answer':answer_set[0]['id'],'content': instance.content}
        data = {'from_user': -1, 'message': push_data, 'time': now_time, 'type': 1}
        notification_user(to_user, data)

    elif type == 4:
        #  美食讨论评论
        disscus_set = Discuss.objects.filter(foodcomment=instance).values('food__name', 'id', 'title')
        push_data = {'user': from_user.pk, 'user_nick_name': user_nick_name, 'user_head_portrait': user_head_portrait,
                     'discuss': disscus_set[0]['id'], 'discuss_title': disscus_set[0]['title'],
                     'discuss_food_name': disscus_set[0]['food__name'], 'content': instance.content}

        data = {'from_user': -1, 'message': push_data, 'time': now_time, 'type': 4}
        notification_user(to_user, data)

    elif type == 5:
        # 讨论回复
        disscus_set = Discuss.objects.filter(foodcomment__foodrevert=instance).values('food__name', 'id', 'title')
        comment_set = FoodComment.objects.filter(foodrevert=instance).values('id')
        push_data = {'user': from_user.pk, 'user_nick_name': user_nick_name, 'user_head_portrait': user_head_portrait,
                     'discuss': disscus_set[0]['id'], 'discuss_title': disscus_set[0]['title'],
                     'discuss_food_name': disscus_set[0]['food__name'], 'comment': comment_set[0]['id'],'content':instance.content
                     }
        data = {'from_user': -1, 'message': push_data, 'time': now_time, 'type': 5}
        notification_user(to_user, data)

    elif type == 6:
        # 系统消息
        data = {'from_user': -1, 'message': content, 'time': now_time, 'type': 6}
        notification_user(to_user, data)


@app.task
def calculate_question_and_sync(question_id):
    """
    计算问题的热度值,并将相关数据同步至数据库
    参数:question_id(问题id)
    执行时间:第二天半夜1点
    """
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')  # 昨天的时间字符串
    today = datetime.now()
    coon = redis.Redis(connection_pool=POOL)
    # 获取问题数据
    question_data = coon.hmget('qd:'+str(question_id)+':'+yesterday,'scan','answer','approval','attention','comment',
                               'collect','school')
    school_id = question_data[6]
    # 检查改问题是否在榜上。zscore返回成员的分数,若不存在改成员就返回None,时间复杂度O(1)
    is_record_exist = coon.zscore('hot:record',question_id)

    # 只有不在该学校的热榜上的问题才能上榜
    if not is_record_exist:
        today = datetime.now().strftime('%Y%m%d')
        scan_num,answer_num,approval_num,attention_num,comment_num,collect_num = question_data[0],question_data[1],question_data[2],question_data[3],question_data[4],question_data[5]
        # 计算热度值
        score = calculate_question_hot_score(scan_num,answer_num,approval_num,attention_num,collect_num,collect_num)
        # 检查是否已经设置(计算该学校热榜帮名)的定时任务
        is_exist = coon.exists('hot:' + str(school_id) + ':' + today)
        if not is_exist:
            execute_time = datetime.utcfromtimestamp(datetime(today.year, today.month, today.day, 1, 20, 0).timestamp())
            calculate_school_hot_rank.apply_async(args=[school_id],eta=execute_time)
        # 添加到对应学校的热榜
        coon.zadd('hot:' + str(school_id) + ':' + today, {question_id: score})

    # 无论问题是否上榜,都同步数据到数据库
    try:
        Question.objects.filter(pk=question_id).update(
            attention_number=F('attention_number')+int(attention_num),
            scan_number=F('scan_number')+int(scan_num),
        )
    except:
        pass
    # 删除该问题留存在redis中的数据
    coon.delete('qd:'+str(question_id)+':'+yesterday)


@app.task # 每天凌晨0点20执行
def check_hot_question_expire_time():
    """定时清理已达到过期时间的上过热榜的问题"""
    coon = redis.Redis(connection_pool=POOL)
    # 现在的时间戳
    now_timestamp = time.time()
    # 删除分值小于当前时间戳的值
    coon.zremrangebyscore('hot:record',min=0,max=now_timestamp)


@app.task
def calculate_school_hot_rank(school_id):
    """
    计算出各学校的热榜
    参数:school_id(学校id)
    执行时间:第二天半夜1.20
    """
    coon = redis.Redis(connection_pool=POOL)
    today = datetime.now().strftime('%Y%m%d')
    # 热榜问题的过期时间
    expire_time = (datetime.now() + timedelta(days=2)).timestamp()
    # 热榜问题前15
    hot_list = coon.zrevrange('hot:' + str(school_id) + ':' + today, start=0, end=14)
    dict = {}
    # 构造字典,键为前二十问题id,值为2天之后的时间戳(2天后才能再次上榜)
    for i in hot_list:
        dict[i] = expire_time
    # 将这些问题添加到热榜记录
    coon.zadd('hot:record',dict)
    zset_number = coon.zcard('hot:' + str(school_id) + ':' + today)
    # 将该学校的热榜除了前15全部删除,但是若不足15就不删除
    if zset_number <= 15:
        pass
    else:
        coon.zremrangebyrank('hot:' + str(school_id) + ':' + today, min=0, max=zset_number - 15 - 1)


@app.task
def get_answer_abstract_and_first_image(answer_id):
    """
    获得回答的摘要和第一张图片,并添加到数据库
    参数:回答id
    返回值:无
    """
    # 获得回答的content
    try:
        answer = Answer.objects.get(pk=int(answer_id))
    except Answer.DoesNotExist:
        pass
    else:
        html = base64.decode(answer.content)
        pattern = re.compile("img src='(.*?)'")
        # 获得第一张图片
        img_url = pattern.search(html)
        # 获得回答摘要
        clean_text = BeautifulSoup(html, "lxml").get_text(strip=True)
        if img_url:
            # 保存至数据库
            answer.first_image = img_url[1]
            answer.abstract = clean_text[0:38]+'...'
            answer.save()
        else:
            answer.abstract = clean_text[0:38]+'...'
            answer.save()

