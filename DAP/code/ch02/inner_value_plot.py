"""
@Title        : European Call Option Inner Value Plot
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-01-11 14:52:29
@Description  : 
"""

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'serif'

K = 8_000
S = np.linspace(7_000, 9_000, 100)
h = np.maximum(S - K, 0)

plt.figure()
plt.plot(S, h, lw=2.5)
plt.xlabel('index level $S_t$ at maturity')
plt.ylabel('inner value of European call option')
plt.grid(True)
plt.title('Inner value of European call option at maturity')
plt.show()
