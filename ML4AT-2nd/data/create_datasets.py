"""
@File         : create_datasets.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-04-08 21:40:50
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import warnings

warnings.filterwarnings("ignore")
from pathlib import Path
import requests
from io import BytesIO
from zipfile import ZipFile, BadZipFile

import numpy as np
import pandas as pd
import pandas_datareader.data as web
from sklearn.datasets import fetch_openml

pd.set_option("display.expand_frame_repr", False)

DATA_STORE = Path("assets.h5")

df = pd.read_csv(
    "./wiki_prices.csv",
    parse_dates=["date"],
    index_col=["date", "ticker"],
    infer_datetime_format=True,
).sort_index()
with pd.HDFStore(DATA_STORE) as store:
    store.put("quandl/wiki/prices", df)

df = pd.read_csv("./wiki_stocks.csv")
with pd.HDFStore(DATA_STORE) as store:
    store.put("quandl/wiki/stocks", df)

# S&P 500 Prices
df = (
    web.DataReader(name="SP500", data_source="fred", start=2009)
    .squeeze()
    .to_frame("close")
)
with pd.HDFStore(DATA_STORE) as store:
    store.put("sp500/fred", df)

sp500_stooq = (
    pd.read_csv("./^spx_d.csv", index_col=0, parse_dates=True)
    .loc["1950":"2019"]
    .rename(columns=str.lower)
)
with pd.HDFStore(DATA_STORE) as store:
    store.put("sp500/stooq", sp500_stooq)

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
df = pd.read_html(url, header=0)[0]
# sec_filings 被舍弃了
df.columns = [
    "ticker",
    "name",
    "gics_sector",
    "gics_sub_industry",
    "location",
    "first_added",
    "cik",
    "founded",
]
df = df.set_index("ticker")
with pd.HDFStore(DATA_STORE) as store:
    store.put("sp500/stocks", df)


df = pd.read_csv("./us_equities_meta_data.csv")
with pd.HDFStore(DATA_STORE) as store:
    store.put("us_equities/stocks", df.set_index("ticker"))

mnist = fetch_openml("mnist_784", version=1)
mnist_path = Path("mnist")
if not mnist_path.exists():
    mnist_path.mkdir()
np.save(mnist_path / "data", mnist.data.astype(np.uint8))
np.save(mnist_path / "label", mnist.target.astype(np.uint8))

# Fashion MNIST Image Data
fashion_mnist = fetch_openml(name="Fashion-MNIST")
label_dict = {
    0: "T-shirt/top",
    1: "Trouser",
    2: "Pullover",
    3: "Dress",
    4: "Coat",
    5: "Sandal",
    6: "Shirt",
    7: "Sneaker",
    8: "Bag",
    9: "Ankle boot",
}
fashion_path = Path("fashion_mnist")
if not fashion_path.exists():
    fashion_path.mkdir()
pd.Series(label_dict).to_csv(fashion_path / "label_dict.csv", index=False, header=None)
np.save(fashion_path / "data", fashion_mnist.data.astype(np.uint8))
np.save(fashion_path / "labels", fashion_mnist.target.astype(np.uint8))

# Bond Price Indexes
securities = {
    "BAMLCC0A0CMTRIV": "US Corp Master TRI",
    "BAMLHYH0A0HYM2TRIV": "US High Yield TRI",
    "BAMLEMCBPITRIV": "Emerging Markets Corporate Plus TRI",
    # "GOLDAMGBD228NLBM": "Gold (London, USD)",
    "DGS10": "10-Year Treasury CMR",
}
df = web.DataReader(name=list(securities.keys()), data_source="fred", start=2000)
df = df.rename(columns=securities).dropna(how="all").resample("B").mean()
with pd.HDFStore(DATA_STORE) as store:
    store.put("fred/assets", df)
