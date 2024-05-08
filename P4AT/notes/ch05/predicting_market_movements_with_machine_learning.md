# 通过机器学习预测市场动向

## 使用线性回归进行市场走势预测

### 价格预测的基本思想

基于时间序列数据的价格预测必须处理一个特殊功能：数据的基于时间的顺序。一般来说，数据的顺序对于线性回归的应用并不重要。

```python
x = np.linspace(0, 10)
y = x + np.random.standard_normal(len(x))

reg = np.polyfit(x, y, deg=1)

plt.figure(figsize=(10, 6))
plt.plot(x, y, "bo", label="data")
plt.plot(x, np.polyval(reg, x), "r", lw=2.5, label="Linear Regression")
```

然而，例如，在预测明天的指数水平时，以正确的顺序排列历史指数水平似乎至关重要。如果是这种情况，那么我们将尝试根据今天、昨天、前一天等的指数水平来预测明天的指数水平。用作输入的天数通常称为**滞后**。因此，使用今天的指数水平和之前的另外两个指数水平会转化为三个滞后。

NumPy 线性代数子包 (linalg) 中有一个函数可以解决一般最小二乘问题：`lstsq`。仅需要结果数组的第一个元素，因为它包含最佳回归参数：
