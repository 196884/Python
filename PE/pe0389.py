from decimal import *
getcontext().prec = 30

def m1(k):
    return Decimal(k+1) / Decimal(2)

def m2(k):
    return Decimal(k*k - 1) / Decimal(3)

def solve():
    # Composition of probability generating functions, then differentiation
    e1  = m1(20) * m1(12) * m1(8) * m1(6) *  m1(4)
    e2  = m2(4) * (m1(6) * m1(8) * m1(12) *  m1(20)) ** 2
    e2 += m1(4) * m2(6) * (m1(8) * m1(12) *  m1(20)) ** 2
    e2 += m1(4) * m1(6) * m2(8) * (m1(12) *  m1(20)) ** 2
    e2 += m1(4) * m1(6) * m1(8) * m2(12)  * (m1(20)) ** 2
    e2 += m1(4) * m1(6) * m1(8) * m1(12)  *  m2(20)
    r = e2 + e1 - e1 ** 2
    print r
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
