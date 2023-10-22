"""
@Title: 割线法
@Author(s): Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime: 2023-10-22 14:34:38
@Description: 
"""


def secant(func, a, b, tol=0.001, maxiter=100):
    n = 1
    while n <= maxiter:
        c = b-func(b) * ((b-a)/(func(b)-func(a)))
        if abs(c-b) < tol:
            return c, n
        a, b = b, c
        n += 1
    return None, n


if __name__ == "__main__":

    def y(x): return x**3 + 2.*x**2 - 5.

    root, iterations = secant(y, -5.0, 5.0, 0.00001, 100)
    print("Root is:", root)
    print("Iterations:", iterations)
