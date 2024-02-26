"""
@Title: Event-driven
@Author(s): Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime: 2023-11-15 22:05:09
@Description: SMA 策略
"""

from datetime import datetime
import backtrader as bt
from backtrader_strategies.strategy_utils import get_action_log_string, get_result_log_string, MyBuySell


class SmaStrategy(bt.Strategy):
    params = (('ma_periods', 20), )

    def __init__(self,):
        self.data_close = self.datas[0].close

        self.order = None
        self.sma = bt.ind.SMA(self.datas[0], periods=self.params.ma_periods)

    def log(self, txt: str):
        dt = self.datas[0].datetime.date(0).isoformat()
        print(f'{dt}: {txt}')

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            direction = 'b' if order.isbuy() else 's'
            log_str = get_action_log_string(
                dir=direction, action='e', price=order.executed.price, size=order.executed.size,
                cost=order.executed.cost, commission=order.executed.comm
            )
            self.log(log_str)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Failed')
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(get_result_log_string(gross=trade.pnl, net=trade.pnlcomm))

    def next(self):
        # 如果订单处于待处理状态，不做任何事情
        if self.order:
            return
        if not self.position:
            if self.data_close[0] > self.sma[0]:
                self.log(get_action_log_string(
                    'b', 'c', self.data_close[0], 1))
                self.order = self.buy()
        else:
            if self.data_close[0] < self.sma[0]:
                self.log(get_action_log_string(
                    's', 'c', self.data_close[0], 1))
                self.order = self.sell()

    def start(self):
        print(f"Initial Portfolio Value: {self.broker.get_value():.2f}")

    def stop(self):
        print(f'Final Portfolio Value: {self.broker.get_value():.2f}')


if __name__ == '__main__':
    data = bt.feeds.YahooFinanceData(
        dataname='AAPL',
        fromdate=datetime(2021, 1, 1),
        todate=datetime(2021, 12, 31)
    )
    cerebro = bt.Cerebro(stdstats=False)

    cerebro.adddata(data)
    cerebro.broker.setcash(1000.0)
    cerebro.addstrategy(SmaStrategy)
    cerebro.addobserver(MyBuySell)
    cerebro.addobserver(bt.observers.Value)

    cerebro.run()
