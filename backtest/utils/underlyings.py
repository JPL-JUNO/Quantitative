"""
@File         : underlyings.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-18 15:54:41
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

from pathlib import Path


def get_underlying(dir, pattern="*.csv"):
    for file in Path(dir).glob(pattern):
        yield file.stem
