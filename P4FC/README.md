# [Python for Finance Cookbook, 2nd](https://www.packtpub.com/product/python-for-finance-cookbook-second-edition/9781803243191)

## 获取数据

- Getting data from Yahoo Finance
- Getting data from Nasdaq Data Link（数据时间有限）
- Getting data from Intrinio（一坨💩）
- Getting data from Alpha Vantage
- Getting data from CoinGecko

[Chapter01](https://github.com/JPL-JUNO/Quantitative/blob/main/P4FC/code/ch01_acquiring_financial_data.ipynb) 提供了多种下载金额数据的方法，Yahoo Finance 与 [Alpha Vantage](https://www.alphavantage.co/support/#api-key) 是不错的选择，其中 Alpha Vantage 需要先填写一些基本信息获取 API Token。 [CoinGecko](https://github.com/man-c/pycoingecko) 是获取加密货币不错的 package。

### 其他可选的数据源

- [IEX Cloud](https://iexcloud.io/)
- [Tiingo](https://www.tiingo.com/)
- [CryptoCompare](https://www.cryptocompare.com/)
- [Twelve Data](https://twelvedata.com/)
- [polygon.io](https://polygon.io/)
- [Shrimpy](https://www.shrimpy.io/)

## 依赖的包

pip install git+https://github.com/mementum/backtrader.git#egg=backtrader
