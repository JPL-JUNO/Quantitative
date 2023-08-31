"""
@Title: 超参数调整，可以衡量不同参数下模型的性能
@Author(s): Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime: 2023-08-30 17:31:22
@Description: 
"""

from knn import KNNClassifier
from itertools import product
from numpy import mean


class HyperParameter:
    """超参数的调整"""

    def __init__(self, model: KNNClassifier, parameters: dict[str, list]) -> None:
        """
        超参数调整的类

        Parameters
        ----------
        model : KNNClassifier
            一个模型，需要实现 fit 和 predict 方法
        parameters : dict[str, list]
            参数组成的字典
        """
        self.model = model
        self.parameters = parameters
        self.best_params_dict = {}
        self.best_evaluation = 0

    def fit(self) -> None:
        """
        超参数的拟合

        Raises
        ------
        ValueError
            如果指定的超参数不是模型的参数，将报错
        """
        assert self.model.fit_flg, "模型未训练"
        params: list[str] = []
        for param in self.parameters.keys():
            if param in self.model.get_params():
                params.append(param)
            else:
                raise ValueError(f"模型不存在参数 {param}")

        evaluations = []
        for param_pair in product(*list(self.parameters.values())):
            params_dict = dict(zip(self.parameters.keys(), param_pair))
            self.model.set_params(params_dict)
            predictions = []
            print(params_dict)
            for example in self.model.testing:
                prediction = self.model.predict(example)
                print(prediction, example.label)
                predictions.append(prediction == example.label)
            print(predictions)
            evaluations.append(mean(predictions))
            if mean(predictions) > self.best_evaluation:
                self.best_evaluation = mean(predictions)
                self.best_params_dict = params_dict


if __name__ == '__main__':
    knn = KNNClassifier()
    knn.fit()
    hp = HyperParameter(knn, {'k': [3, 5, 7], 'p': [1, 2]})
    hp.fit()
