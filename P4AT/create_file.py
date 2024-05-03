"""
@File         : create_file.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-02 14:46:10
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

sections = {
    "ch01": ["Python and Algorithmic Trading"],
    "ch02": ["Python Infrastructure"],
    "ch03": ["Working with Financial Data"],
    "ch04": ["Mastering Vectorized Backtesting"],
    "ch05": ["Predicting Market Movements with Machine Learning"],
    "ch06": ["Building Classes for Event-Based Backtesting"],
    "ch07": ["Working with Real-Time Data and Sockets"],
    "ch08": ["CFD Trading with Oanda"],
    "ch09": ["FX Trading with FXCM"],
    "ch10": ["Automating Trading Operations"],
}


from pathlib import Path

for chapter, section in sections.items():
    code = Path("code") / chapter
    code.mkdir(parents=True, exist_ok=True)
    markdown = Path("notes") / chapter
    markdown.mkdir(parents=True, exist_ok=True)
    for s in section:
        with open(code / (s + ".ipynb"), mode="w+", encoding="utf-8") as f:
            f.close()
        with open(code / (s + ".py"), mode="w+", encoding="utf-8") as f:
            f.close()
        with open(markdown / (s + ".md"), mode="w+", encoding="utf-8") as f:
            f.close()
