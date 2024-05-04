"""
@File         : working_with_financial_data.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-04 17:04:49
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

fn = "../../data/AAPL.csv"
with open(fn, "r") as f:
    for _ in range(5):
        print(f.readline(), end="")

import csv

csv_reader = csv.reader(open(fn, "r"))
data = list(csv_reader)
print(data[:5])

csv_reader = csv.DictReader(open(fn, "r"))
data = list(csv_reader)
print(data[:3])

sum(float(l["CLOSE"]) for l in data) / len(data)

import pandas as pd

data = pd.read_csv(fn, index_col=0, parse_dates=True)
data.info()
