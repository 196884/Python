from decimal import *
getcontext().prec = 50

B = 10 ** 9
n = 1000
p = Decimal(0.5)

def getP(f):
    r = (Decimal(B).ln() - Decimal(n) * ((1 - f).ln())) / ((1 + 2 * f) / (1 - f)).ln()
    return r

def solve():
    # by looking at getP above, one sees that the optimal is for f around 0.15,
    # where you need to win the flip 432 times or more to be a billionaire
    # the solution is just:
    # \sum _{k=432}^1000 Choose(1000, 432) / 2^1000
    b = 432
    factorials = [1, 1]
    for k in range(2, n+1):
        factorials.append(k * factorials[-1])
    
    num = 0
    for k in range(b, n+1):
        num += factorials[n] / (factorials[k] * factorials[n-k])
    r = Decimal(num) / Decimal(2 ** n)
    print r
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
