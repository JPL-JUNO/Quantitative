"""
@Title: 股票期权
@Author(s): Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime: 2023-10-22 20:13:22
@Description: 
"""
import math
import numpy as np
from numpy import ndarray


class StockOption(object):
    def __init__(self, S0, K, r: float = .05, T: int | float = 1, N: int = 2, pu: float = 0, pd: float = 0,
                 div: float = 0, sigma: float = 0, is_put: bool = False, is_am: bool = False) -> None:
        """_summary_

        Parameters
        ----------
        S0 : _type_
            _description_
        K : _type_
            _description_
        r : float, optional
            无风险利率, by default .05
        T : int | float, optional
            到期时间, by default 1
        N : int, optional
            每步中可能的方向, by default 2
        pu : float, optional
            上涨的比率, by default 0
        pd : float, optional
            下跌的比率, by default 0
        div : float, optional
            分红率, by default 0
        sigma : float, optional
            波动率, by default 0
        is_put : bool, optional
            是否是看跌, by default False
        is_am : bool, optional
            是否是美式期权, by default False
        """
        self.S0 = S0
        self.K = K
        self.r = r
        self.T = T
        self.N = max(1, N)
        # declare the stock prices here
        self.STs = []
        self.pu, self.pd = pu, pd
        self.div = div
        self.sigma = sigma
        self.is_call = not is_put
        self.is_european = not is_am

    @property
    def dt(self):
        # 时间步长是由这个类的属性计算的
        return self.T/float(self.N)

    @property
    def df(self):
        # 折现因子也是有这个类的属性计算的
        return math.exp(-(self.r-self.div)*self.dt)


class BinomialEuropeanOption(StockOption):
    def setup_parameters(self):
        self.M = self.N+1  # 最后的价格数（不同结果），因此走了 N ，会产生 N + 1 个价格，但是数量不是 N + 1 个，只是不同个数的值是 N + 1个
        self.u = 1+self.pu  # 在上涨状态下的预期值（上涨的幅度）
        self.d = 1-self.pd  # 在下跌状态下的预期值（并不是概率，应该下跌的百分比）
        self.qu = (math.exp(
            (self.r-self.div)*self.dt)-self.d)/(self.u-self.d)
        self.qd = 1-self.qu

    def init_stock_price_tree(self):
        self.STs = np.zeros(self.M)
        for i in range(self.M):
            self.STs[i] = self.S0 * (self.u ** (self.N - i)) * (self.d ** i)

    def init_payoffs_tree(self):
        if self.is_call:
            # 向量化操作
            return np.maximum(0, self.STs - self.K)
        else:
            return np.maximum(0, self.K - self.STs)

    def traverse_tree(self, payoffs: ndarray) -> ndarray:
        # TODO: 需要判断如何计算的（计算逻辑），似乎有点确定，但是需要进一步想清楚
        for _ in range(self.N):
            payoffs = (payoffs[:-1] * self.qu +
                       payoffs[1:] * self.qd) * self.df
        return payoffs

    def begin_tree_traversal(self):
        payoffs = self.init_payoffs_tree()
        return self.traverse_tree(payoffs)

    def price(self):
        self.setup_parameters()
        self.init_stock_price_tree()
        payoffs = self.begin_tree_traversal()
        return payoffs[0]


class BinomialTreeOption(StockOption):
    def setup_parameters(self):
        self.u = 1+self.pu  # 在上涨状态下的预期值（上涨的幅度）
        self.d = 1-self.pd  # 在下跌状态下的预期值（并不是概率，应该下跌的百分比）
        self.qu = (math.exp(
            (self.r-self.div)*self.dt)-self.d)/(self.u-self.d)
        self.qd = 1-self.qu

    def init_stock_price_tree(self):
        """使用二维 Numpy 数组存储所有时间步长股票价格的预期收益，该信息用于计算每个期间行权的收益值"""
        self.STs = [np.array([self.S0])]
        for _ in range(self.N):
            prev_branches = self.STs[-1]
            st = np.concatenate((
                prev_branches*self.u,
                [prev_branches[-1]*self.d]
            ))
            self.STs.append(st)

    def init_payoffs_tree(self):
        """将收益树创建为二维NumPy数组，以期权到期时的内在价值为起始点"""
        # TODO: 没办法确定方法的计算逻辑
        if self.is_call:
            return np.maximum(0, self.STs[self.N]-self.K)
        else:
            return np.maximum(0, self.K-self.STs[self.N])

    def check_early_exercise(self, payoffs, node):
        """在提前行权与不行权间返回最大收益值"""
        if self.is_call:
            return np.maximum(payoffs, self.STs[node]-self.K)
        else:
            return np.maximum(payoffs, self.K-self.STs[node])

    def traverse_tree(self, payoffs):
        """调用 check_early_exercise() 以检查在任意时间步长中提前行权可获得的最佳收益"""
        for i in reversed(range(self.N)):
            payoffs = (payoffs[:-1]*self.qu+payoffs[1:]*self.qd)*self.df
            if not self.is_european:
                payoffs = self.check_early_exercise(payoffs, i)
        return payoffs

    def begin_tree_traversal(self):
        payoffs = self.init_payoffs_tree()
        return self.traverse_tree(payoffs)

    def price(self):
        self.setup_parameters()
        self.init_stock_price_tree()
        payoffs = self.begin_tree_traversal()
        return payoffs[0]


class BinomialCRROption(BinomialTreeOption):
    def setup_parameters(self):
        self.u = math.exp(self.sigma*math.sqrt(self.dt))
        self.d = 1./self.u
        self.qu = (math.exp((self.r-self.div)*self.dt) -
                   self.d) / (self.u - self.d)
        self.qd = 1 - self.qu


class BinomialLROption(BinomialTreeOption):
    def setup_parameters(self):
        odd_N = self.N if (self.N % 2 == 0) else (self.N + 1)
        d1 = (math.log(self.S0/self.K) +
              ((self.r-self.div)+(self.sigma**2)/2.)*self.T)/(self.sigma*math.sqrt(self.T))
        d2 = (math.log(self.S0/self.K) +
              ((self.r-self.div)-(self.sigma**2)/2.)*self.T)/(self.sigma*math.sqrt(self.T))
        pbar = self.pp_2_inversion(d1, odd_N)
        self.p = self.pp_2_inversion(d2, odd_N)
        self.u = 1./self.df*pbar/self.p
        self.d = (1/self.df-self.p*self.u)/(1-self.p)
        self.qu = self.p
        self.qd = 1 - self.p

    def pp_2_inversion(self, z, n):
        return .5 + math.copysign(1, z) *\
            math.sqrt(.25-.25*math.exp(-((z/(n+1./3.+.1/(n+1)))**2.)*(n+1./6.)
                                       )
                      )


if __name__ == '__main__':
    eu_option = BinomialEuropeanOption(
        50, 52, r=0.05, T=2, N=2, pu=0.2, pd=0.2, is_put=True)
    print('European put option price is:', eu_option.price())

    am_option = BinomialTreeOption(
        50, 52, r=0.05, T=2, N=2, pu=.2, pd=.2, is_put=True, is_am=True
    )
    print('American put option price is:', am_option.price())

    # CRR 模型定价
    eu_option = BinomialCRROption(
        50, 52, r=0.05, T=2, N=2, sigma=0.3, is_put=True)
    print('European put:', eu_option.price())

    am_option = BinomialCRROption(
        50, 52, r=0.05, T=2, N=2, sigma=0.3, is_put=True, is_am=True)
    print('American put option price is:', am_option.price())

    eu_option = BinomialLROption(
        50, 52, r=0.05, T=2, N=4, sigma=0.3, is_put=True)
    print('European put:', eu_option.price())
    am_option = BinomialLROption(
        50, 52, r=0.05, T=2, N=4, sigma=0.3, is_put=True, is_am=True)
    print('American put:', am_option.price())
