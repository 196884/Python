from decimal import *
getcontext().prec = 50

def choose(n, k, fl):
    return fl[n] / fl[k] / fl[n-k]

def solve():
    """
    There's a simple induction: if f(n) is the expected time to get from 0 to 2^n-1, then:
    f(0) = 0
    f(n) = (\sum _{k=0}^n Choose(n, k) f(k)) / 2^k
    """
    fact = [1, 1]
    for k in range(2, 33):
        fact.append(k * fact[-1])

    f = [0]
    for n in range(1, 33):
        num = 2 ** n 
        for k in range(0, n):
            num += choose(n, k, fact) * f[k]
        f.append(Decimal(num) / Decimal(2 ** n - 1))
    print f[-1]
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
