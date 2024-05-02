"""
@File         : 7_cal_vix.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-02-26 22:20:46
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

from calculating_vix.read_file import read_file

data_path = "./data/SPX_EOD_2018_10_15.csv"

meta_rows, call_and_puts = read_file(data_path)
for line in meta_rows:
    print(line)
