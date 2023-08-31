"""
@Title: 数据加载器
@Author(s): Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime: 2023-08-30 21:06:16
@Description: 
"""
from sample import LabeledSample


class DataLoader:
    """数据加载器，将数据切分为训练和测试"""

    def __init__(self):
        self.training: list[LabeledSample] = []
        self.testing: list[LabeledSample] = []

    def load(self, raw_data: list[dict[str, float]]) -> None:
        """
        加载数据

        Parameters
        ----------
        raw_data : list[dict[str, float]]
            原始数据，需要保存在一个列表中，以字典的形式

        Returns
        -------
        None
            没有显式返回值
        """
        for n, data in enumerate(raw_data):
            try:
                if n % 5 == 0:
                    # 样本中保留 20% 作为测试（验证）数据，来确定超参数（k 和 distance 的计算方式）
                    test = LabeledSample.from_dict(data)
                    self.testing.append(test)
                else:
                    train = LabeledSample.from_dict(data)
                    self.training.append(train)
            except:
                print(f"第 {n+1} 条数据出现错误！")
                return None
