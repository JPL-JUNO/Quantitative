import numpy.random as npr
import numpy as np


def gen_sn(M: int, I: int, anti_paths: bool = True, mo_match: bool = True):
    """生成随机数进行模型

    Parameters
    ----------
    M : int
        number of time intervals for discretization
    I : int
        number of paths to be simulated
    anti_paths : bool, optional
        使用对立变量, 为了将均值变为 0 , by default True
    mo_match : bool, optional
        使用矩匹配, by default True

    Returns
    -------
    _type_
        _description_
    """
    if anti_paths:
        sn = npr.standard_normal((M + 1, int(I / 2)))
        sn = np.concatenate((sn, -sn), axis=1)
    else:
        sn = npr.standard_normal((M + 1, I))
    if mo_match:
        sn = (sn - sn.mean()) / sn.std()
    return sn


def gbm_mcs_stat(K):
    sn = gen_sn(1, I)
    ST = 0


def gbm_mcs_dyna(K, option="call"):

    pass
