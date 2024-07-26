import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from datetime import date, timedelta

n_days = 256

r_f = 2.0
n_cluster = 10
n_class = 5
r_day = 16

now = date.today()

all_fund: pd.DataFrame = get_all_securities("fund", now)
funds = all_fund[all_fund.start_date < now - timedelta(days=365)].index.tolist()

history(n_days, "1d", "money", funds).mean()

p = history(n_days, "1d", "close", funds).dropna(axis=1)

returns = p.apply(np.log).diff().dropna()
X = returns.T

model = KMeans(n_clusters=n_cluster).fit(returns)
y_pred = model.predict(X)

res = pd.DataFrame(y_pred, index=p.columns, columns=["Cluster"])
res.groupby("Cluster", sort=False)
