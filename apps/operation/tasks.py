import redis


from HotSchool.celery import app
from HotSchool.settings import POOL
from question.algorithms import wilson_score_answer
from question.models import Answer


@app.task
def calculate_answer_score(question_id,answer_id):
    """
    更新回答的威尔逊得分,同时将数据刷回数据库(15分钟后)
    :param question_id: 问题id
    :param answer_id: 回答id
    :return: 无
    """
    coon = redis.Redis(connection_pool=POOL)
    # 获取回答数据,若不存在就说明回答被删除了,无需同步
    answer_data = coon.hmget('ad:' + str(answer_id),'approval','vote','collect')
    if answer_data:
        approval_number,vote_number,collect_number = int(answer_data[0]),int(answer_data[1]),int(answer_data[2])
        answer_score = wilson_score_answer(approval_number,vote_number)
        # 同步数据库
        Answer.objects.filter(pk=answer_id).update(approval_number=approval_number,vote_number=vote_number,
                                                   collect_number=collect_number)
        # 更新回答分数
        coon.zadd('answer:score:'+str(question_id),{answer_id:answer_score})
        # 删除该回答留存在redis中的数据
        coon.delete('ad:' + str(answer_id))






