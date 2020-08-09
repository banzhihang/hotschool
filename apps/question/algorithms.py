import numpy as np


def wilson_score_answer(u, n, zP=2.):
    """
    回答威尔逊得分(Wilson Score)排序算法 => 计算威尔逊得分
    :param u: 好评数
    :param n: 评论总数
    :param zP: 正太分布的分位数(zP一般取值2即可，即95%的置信度)
    :return: 威尔逊得分
    """
    pos_rat = u * 1. / n * 1.
    score = (pos_rat + (np.square(zP) / (2. * n))
             - ((zP / (2. * n)) * np.sqrt(4. * n * (1. - pos_rat) * pos_rat + np.square(zP)))) / (1. + np.square(zP) / n)
    return score


def calculate_question_hot_score(scan_num,answer_num,approval_num,attention_num,comment_num,collect_num):
    """
    计算问题的热度值
    :param scan_num: 浏览增量
    :param answer_num: 回答增量
    :param approval_num: 赞同增量
    :param attention_num: 收藏(关注)增量
    :param comment_num: 评论增量
    :param collect_num:该问题的回答的收藏增量
    :return: 问题的热度值
    """
    score = int(scan_num)*0.35+int(answer_num)*0.25+int(attention_num)*0.2+int(approval_num)*0.1+\
            int(comment_num)*0.05+int(collect_num)*0.05
    return float(score)

