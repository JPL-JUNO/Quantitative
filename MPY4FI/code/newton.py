"""
@Title: 
@Author(s): Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime: 2023-10-22 14:21:58
@Description: 
"""


def newton(func, df, x, tol=.001, maxiter=100):
    n = 1
    while n < maxiter:
        x1 = x - func(x)/df(x)
        if abs(x1 - x) < tol:
            return x1, n
        x = x1
        n += 1
    return None, n


if __name__ == '__main__':
    def y(x): return x**3 + 2*x**2 - 5
    def dy(x): return 3*x**2 + 4*x
    root, iterations = newton(y, dy, 5.0, 0.00001, 100)
    print('Root is:', root)
    print('Iterations is:', iterations)
