import numpy as np

def wilson_score_food(vote_all_score, n, zP=2.):
    """
    美食威尔逊得分(Wilson Score)排序算法 => 计算威尔逊得分
    :param vote_all_score: 投票总分
    :param n: 投票人数
    :param zP: 正太分布的分位数(zP一般取值2即可，即95%的置信度)
    :return: 威尔逊得分
    """
    pos_rat = (vote_all_score/n)/5 # 为最高分,这里是计算好评率,即平均得分除以最高分5分
    score = (pos_rat + (np.square(zP) / (2. * n))
             - ((zP / (2. * n)) * np.sqrt(4. * n * (1. - pos_rat) * pos_rat + np.square(zP)))) / (1. + np.square(zP) / n)
    # 若威尔逊得分小于0.1,则设为0.1,保证结果分不会小于1分

    if 30<n<=100:
        score -= 0.1
    elif n<=30:
        score -= 0.15
    if score <=0.1:
        return 1.0

    return score*10
