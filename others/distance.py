"""
@Title: 提供对距离计算的类
@Author(s): Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime: 2023-08-30 15:54:21
@Description: 
"""
from sample import Sample


class Distance:
    """
    实现距离的计算的超类
    """

    def distance(self, s1: Sample, s2: Sample) -> float:
        """距离超类不实现具体的方法，实现交给子类根据不同的需要取实现

        Parameters
        ----------
        s1 : Sample
            计算距离的一个样本
        s2 : Sample
            计算距离的另一个样本

        Returns
        -------
        float
            两个样本之间的距离（距离的实现看具体的子类）

        Raises
        ------
        NotImplementedError
            超类没有实现具体方法
        """
        raise NotImplementedError


class Chebyshev(Distance):
    """提供对切比雪夫距离的实现"""
    pass


class Minkowski(Distance):
    """
    因为欧式距离（p=2）和曼哈顿距离（p=1）都是 Minkowski 距离的特殊情况，因此写一个超类
    """
    p = int

    def distance(self, s1: Sample, s2: Sample) -> float:
        dis = sum([abs(s1.sepal_length - s2.sepal_length)**self.p,
                   abs(s1.sepal_width - s2.sepal_width)**self.p,
                   abs(s1.petal_length - s2.petal_length)**self.p,
                   abs(s1.petal_width - s2.petal_width)**self.p
                   ]
                  )
        return dis ** (1 / self.p)


class Euclidean(Minkowski):
    p = 2


class Manhattan(Minkowski):
    p = 1
