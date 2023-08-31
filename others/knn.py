"""
@Title: KNN 类的实现
@Author(s): Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime: 2023-08-30 20:28:11
@Description: 可以初始化、训练和预测
"""
from distance import Euclidean, Manhattan
from sample import LabeledSample, Sample
from operator import itemgetter
from collections import Counter


class KNNClassifier:
    def __init__(self, k: int = 3, p: int = 2) -> None:
        """
        初始化分类器

        Parameters
        ----------
        k : int, optional
            近邻的个数，超参数。如果是二分类建议使用奇数, by default 3
        p : int, optional
            距离的计算方式，默认采用欧式距离, by default 2

        Raises
        ------
        NotImplementedError
            仅提供欧式距离或曼哈顿距离，其余报未实现错误
        """
        self.p = p
        if self.p == 2:
            self.distance_algorithm = Euclidean()
        elif self.p == 1:
            self.distance_algorithm = Manhattan()
        else:
            raise NotImplementedError
        self.k = k
        self._model_params = {'k': self.k, 'p': self.p}
        self.fit_flg = False
        self.training: list[LabeledSample] = []
        self.testing: list[LabeledSample] = []

    # def fit(self, X, y) -> None:
    #     pass

    def fit(self,
            training_data: list[LabeledSample],
            testing_data: list[LabeledSample]) -> None:
        """
        模型训练，因为 KNN 不需要拟合，没有参数（权重）的返回值

        Parameters
        ----------
        training_data : list[LabeledSample]
            训练集
        testing_data : list[LabeledSample]
            测试集

        Raises
        ------
        RuntimeError
            训练集，测试集  不能未空
        """
        if not training_data or not testing_data:
            raise RuntimeError("数据或特征为空")
        # assert len(training_X) == len(training_y), "特征与标签的长度不同"
        self.fit_flg = True
        self.training = training_data
        self.testing = testing_data

    def predict(self, predict_data: Sample) -> str:
        """
        预测样本的类别

        Parameters
        ----------
        predict_data : Sample
            待预测样本

        Returns
        -------
        str
            预测值

        Raises
        ------
        ValueError
            模型没有训练将报错
        """
        if not self.fit_flg:
            raise ValueError(f"没有训练模型可用")
        distances: list[float] = []
        for n, training_data in enumerate(self.training):
            distance = self.distance_algorithm.distance(
                predict_data, training_data)
            distances.append({"index": n, "distance": distance})
        distances.sort(key=itemgetter("distance"))
        top_k_index = [item["index"] for item in distances[:self.k]]
        top_k_label = [self.training[index].label for index in top_k_index]
        frequency: Counter[str] = Counter(top_k_label)
        label, *_ = frequency.most_common()
        return label[0]

    def get_params(self) -> dict:
        """
        返回模型的一些参数

        Returns
        -------
        dict
            模型参数字典
        """
        return self._model_params

    def set_params(self, params: dict) -> None:
        """
        设置参数，将使用 __dict__ 修改模型的参数，主要是为了在超参数调整时改变模型参数

        Parameters
        ----------
        params : dict
            参数字典

        Raises
        ------
        KeyError
            如果提供了非模型参数，将报错
        """
        for key, value in params.items():
            if key not in self._model_params:
                raise KeyError("模型没有该参数")
            else:
                self.__dict__[key] = value
        self._model_params = {'k': self.k, 'p': self.p}


if __name__ == '__main__':
    model = KNNClassifier(k=3, p=2)
