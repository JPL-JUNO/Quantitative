# Machine Learning for Algorithmic Trading - Second Edition

Predictive models to extract signals from market and alternative data for systematic trading strategies with Python

## 关于数据问题

1. wiki_prices.csv
    - 说明
    - 官方的下载地址[点击这里](<https://data.nasdaq.com/tables/WIKIP/WIKI-PRICES/export>)或者本人的网盘连接[点击这里]()
2. ^spx_d.csv
    - 说明
    - 下载地址，仓库中已经提供了[^spx_d.csv](./data/^spx_d.csv)
3. wiki_stocks.csv

## 安装 `zipline`

[zipline](https://pypi.org/project/zipline/) 是一个 Python 算法交易库。它是一个用于回测的事件驱动系统。zipline 目前在生产中用作回溯测试和实时交易引擎，为 Quantopian 提供支持——Quantopian 是一个免费的、以社区为中心的托管平台，用于构建和执行交易策略。Quantopian 还为专业人士提供全面托管的服务，包括 zipline、Alphalens、Pyfolio、FactSet 数据等。

### 特征

- 易于使用：zipline 试图摆脱你的束缚，以便你可以专注于算法开发。
- 开箱即用：可以从用户编写的算法中轻松访问许多常见的统计数据，例如移动平均值和线性回归。
- [PyData](https://pydata.org/) 集成：历史数据的输入和性能统计的输出基于 Pandas DataFrames，可以很好地集成到现有的 PyData 生态系统中。
- 统计和机器学习库：可以使用 matplotlib、scipy、statsmodels 和 sklearn 等库来支持最先进交易系统的开发、分析和可视化。

### 安装步骤

1. 确保你已经安装 conda
2. 创建新的环境并激活环境

```conda
conda create -n env_name python=3.9
```

`env_name` 请修改为自己的环境名（自己定义）

```conda
conda activate env_name
```

python 的版本需要大于 3.9，因为不然的话找不到 `zoneinfo` 内置库，这个库由 python3.9 引入
3. 安装 `zipline-reloaded`

```conda
conda install -c conda-forge zipline-reloaded
```
