from decimal import *
getcontext().prec = 30

def cf(r, n):
    num = 900 * (1 - r) * (1 - r**n) - 3 * (1 - (n+1) * r**n + n * r ** (n+1))
    den = (1-r) ** 2
    return num / den

def foo(r):
    return cf(r, 5000) + 600000000000

def solve():
    low = Decimal(1.001)
    high = Decimal(1.1)
    for n in range(0, 1000):
        m = (low + high) / Decimal(2)
        if foo(m) < 0:
            high = m
        else:
            low = m
    print low
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
