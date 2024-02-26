"""
@File         : read_file.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-02-26 22:11:51
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import csv, glob

META_DATA_ROWS = 3
COLS = 7

# 文件的前三行是这些元数据
# SPX (S&P 500 INDEX),2750.79,-16.34
# Oct 15 2018 @ 20:00 ET
# Calls,Last Sale,Net,Bid,Ask,Vol,Open Int,Puts,Last Sale,Net,Bid,Ask,Vol,Open Int


def read_file(filepath):
    """提供对单个文件的读取

    Parameters
    ----------
    filepath : _type_
        文件路径

    Returns
    -------
    _type_
        _description_
    """
    meta_rows = []
    calls_and_puts = []
    with open(filepath, "r") as file:
        reader = csv.reader(file)
        for row, cells in enumerate(reader):
            if row < META_DATA_ROWS:
                meta_rows.append(cells)
            else:
                # Calls,Last Sale,Net,Bid,Ask,Vol,Open Int
                call = cells[:COLS]
                # Puts,Last Sale,Net,Bid,Ask,Vol,Open Int
                put = cells[COLS:-1]
                calls_and_puts.append((call, put))
    return (meta_rows, calls_and_puts)
