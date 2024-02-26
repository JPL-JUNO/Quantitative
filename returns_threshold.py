"""
@Title        : 在给定的 Greeks 下，PV 和 IV 的变动对收益的影响，short options
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2023-12-08 21:54:00
@Description  : 假定对冲是完全的（或者不考虑对冲的缺口）
"""

import numpy as np
import matplotlib.pyplot as plt

iv = np.arange(-3, 3.1, .1)
pv = np.arange(-3, 3.1, .1)

DELTA = 0
GAMMA = -24000
VEGA = -50000
THETA = 10000
UNDERLYING = 0

xx, yy = np.meshgrid(iv, pv)

zz = xx ** 2 * GAMMA + yy * VEGA + THETA + DELTA + UNDERLYING

cs = np.sort(np.append(0, np.linspace(np.min(zz), np.max(zz), 10)))
fig, ax = plt.subplots(figsize=(8, 6))
cset = ax.contourf(xx, yy, zz, alpha=.5)
contour = ax.contour(
    xx, yy, zz, colors='k')
ax.set_xlabel('PV')
ax.set_ylabel('IV')
ax.clabel(contour, colors='r')
ax.plot([-2.39], [2.5], 'g*', markersize=10)
plt.colorbar(cset)
plt.tight_layout()
