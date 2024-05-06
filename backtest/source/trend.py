"""
@File         : trend.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-24 21:54:26
@Email        : cuixuanstephen@gmail.com
@Description  : 趋势指标回测
"""


class Trend:
    def __init__(self, train_size: float = 0.8, short=False) -> None:
        self.train_size = train_size
        self.short = short
        pass

    def load_data(self):
        raise NotImplementedError

    def backtest(self):
        raise NotImplementedError

    def test_backtest(self):
        raise NotImplementedError

    def plot_results(self):
        raise NotImplementedError
