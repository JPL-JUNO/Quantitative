"""
@File         : Simulation.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-02-17 15:46:40
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import numpy.random as npr
import numpy as np
import matplotlib.pyplot as plt
from print_info import PrintInfo


class Simulation:
    def __init__(self, S0, M, I, T, theta=0.02, kappa=3, sigma=0.1, v0=0.1, r=0.05):
        self.S0 = S0
        self.M = M
        self.I = I
        self.T = T
        self.dt = T / M
        self.theta = theta
        self.kappa = kappa
        self.sigma = sigma
        self.v0 = v0
        self.r = r
        self.print_info = PrintInfo()

    def srd_euler(self, theta, kappa, sigma):
        """_summary_

        Parameters
        ----------
        kappa : _type_
            均值回归因子
        theta : _type_
            长期过程均值
        sigma : _type_
            恒定波动率参数

        Returns
        -------
        None
        """
        xh = np.zeros((self.M + 1, self.I))
        self.x = np.zeros_like(xh)
        xh[0] = self.S0
        self.x[0] = self.S0
        for t in range(1, self.M + 1):
            xh[t] = (
                xh[t - 1]
                + kappa * (theta - np.maximum(xh[t - 1], 0)) * self.dt
                + sigma
                * np.sqrt(np.maximum(xh[t - 1], 0))
                * np.sqrt(self.dt)
                * npr.standard_normal(self.I)
            )
        self.x = np.maximum(xh, 0)

    def srd_exact(self, theta, kappa, sigma):
        self.x = np.zeros((self.M + 1, self.I))
        self.x[0] = self.S0
        for t in range(1, self.M + 1):
            df = 4 * theta * kappa / sigma**2
            c = (sigma**2 * (1 - np.exp(-kappa * self.dt))) / (4 * kappa)
            nc = np.exp(-kappa * self.dt) / c * self.x[t - 1]
            self.x[t] = c * npr.noncentral_chisquare(df, nc, size=self.I)

    def stochastic_volatility(self, cho_mat):
        # 生成三维随机数数据集
        ran_num = npr.standard_normal((2, self.M + 1, self.I))
        v = np.zeros_like(ran_num[0])
        vh = np.zeros_like(v)
        v[0] = self.v0
        vh[0] = self.v0

        for t in range(1, self.M + 1):
            # 选择相关的随机数子集，并通过柯列斯基矩阵转换
            ran = np.dot(cho_mat, ran_num[:, t, :])
            # 根据欧拉格式模拟路径
            vh[t] = (
                vh[t - 1]
                + self.kappa * (self.theta - np.maximum(vh[t - 1], 0)) * self.dt
                + self.sigma
                * np.sqrt(np.maximum(vh[t - 1], 0))
                * np.sqrt(self.dt)
                * ran[1]
            )

        self.v = np.maximum(vh, 0)
        S = np.zeros_like(ran_num[0])

        S[0] = self.S0
        for t in range(1, self.M + 1):
            ran = np.dot(cho_mat, ran_num[:, t, :])
            S[t] = S[t - 1] * np.exp(
                (self.r - 0.5 * self.v[t]) * self.dt
                + np.sqrt(self.v[t]) * ran[0] * np.sqrt(self.dt)
            )

        self.S = S

    def plot(self, *args):
        n = len(args)
        fig, axes = plt.subplots(1, n)
        for i, ax in enumerate(axes):
            ax.hist(args[i], bins=50)
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        plt.tight_layout()
        return fig, axes

    def plot_path(self):
        fig = plt.figure(figsize=(10, 6))
        plt.plot(self.x[:, :10], lw=1.5)
        plt.xlabel("Time")
        plt.ylabel("Index Level")
