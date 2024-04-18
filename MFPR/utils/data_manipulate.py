"""
@File         : data_manipulate.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-17 20:50:57
@Email        : cuixuanstephen@gmail.com
@Description  : 数据操作
"""

import numpy as np


def add_column(data: np.ndarray, times: int) -> np.ndarray:
    """

    Parameters
    ----------
    data : np.ndarray
        原始数据
    times : int
        新增列数

    Returns
    -------
    np.ndarray
        添加列后的数据
    """
    new = np.zeros(shape=(len(data), times), dtype=float)
    data = np.append(data, new, axis=1)
    return data


def delete_column(data: np.ndarray, index: int, times: int) -> np.ndarray:
    for _ in range(1, times + 1):
        data = np.delete(data, index, axis=1)
    return data


def delete_row(data: np.ndarray, number: int) -> np.ndarray:
    data = data[number:]
    return data
