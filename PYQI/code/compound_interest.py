import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1)
data = pd.DataFrame({"frequency": np.arange(1, 15)})
data["final_value"] = 100 * (1 + 0.1 / data["frequency"]) ** data["frequency"]
data.plot(x="frequency", y="final_value", style="o-", ax=ax)
ax.hlines(100 * np.exp(0.1), xmin=0, xmax=15, linestyles="--")
