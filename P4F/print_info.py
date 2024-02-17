"""
@File         : print_info.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-02-17 16:01:33
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

import scipy.stats as scs
import numpy as np


class PrintInfo:
    def __init__(self) -> None:
        pass

    def print_statistics(self, x1, x2):
        sta1 = scs.describe(x1)
        sta2 = scs.describe(x2)
        print(f"{'statistic':>14} {'data set 1':>14} {'data set 2':>14}")
        print(45 * "-")
        print(f"{'size':>14} {sta1[0]:>14.3f} {sta2[0]:>14.3f}")
        print(f"{'min':>14} {sta1[1][0]:>14.3f} {sta2[1][0]:>14.3f}")
        print(f"{'max':>14} {sta1[1][1]:>14.3f} {sta2[1][1]:>14.3f}")
        print(f"{'mean':>14} {sta1[2]:>14.3f} {sta2[2]:>14.3f}")
        print(f"{'std':>14} {np.sqrt(sta1[3]):>14.3f} {np.sqrt(sta2[3]):>14.3f}")
        print(f"{'skew':>14} {sta1[4]:>14.3f} {sta2[4]:>14.3f}")
        print(f"{'kurtosis':>14} {sta1[5]:>14.3f} {sta2[5]:>14.3f}")
