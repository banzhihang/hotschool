import numpy as np


def wilson_score(u, n, zP=2.):
    """
    威尔逊得分(Wilson Score)排序算法 => 计算威尔逊得分
    :param u: 好评数
    :param n: 评论总数
    :param zP: 正太分布的分位数(zP一般取值2即可，即95%的置信度)
    :return: 威尔逊得分
    """
    pos_rat = u * 1. / n * 1.
    score = (pos_rat + (np.square(zP) / (2. * n))
             - ((zP / (2. * n)) * np.sqrt(4. * n * (1. - pos_rat) * pos_rat + np.square(zP)))) / (1. + np.square(zP) / n)
    return score
