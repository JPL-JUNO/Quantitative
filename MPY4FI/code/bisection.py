"""
@Title: 
@Author(s): Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime: 2023-10-21 22:58:16
@Description: 
"""


def bisection(func, a, b, tol: float = .1, maxiter: int = 10):
    n = 1
    while n <= maxiter:
        c = (a+b)*.5
        if func(c) == 0 or abs(a-b)*.5 < tol:
            # 若 f(c) = 0 或在预设的误差容忍范围内接近零点，可视为根已求出。
            return c, n
        n += 1
        if func(c) * func(a) < 0:
            a, b = a, c
        else:
            a, b = c, b
    return c, n


def y(x): return x ** 3 + 2.*x**2-5


if __name__ == '__main__':
    root, iterations = bisection(y, -5, 5, .00001, 100)
    print("Root is:", root)
    print("Iterations:", iterations)
