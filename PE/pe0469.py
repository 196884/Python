from fractions import Fraction
from decimal import *

getcontext().prec = 60

cache = dict()

def F(N):
    if N == 1:
        return Fraction(0, 1)
    if N == 2:
        return Fraction(1, 1)
    cached = cache.get(N, None)
    if cached != None:
        return cached
    r = Fraction(0, 1)
    for k in range(1, N-1):
        r += F(k)
    r = 2 * ( r + N - 1 )
    r /= N
    cache[N] = r
    return r

def r(N):
    return (2 + F(N-3))/N

def solve():
    # The fraction converges pretty fast...
    x = r(50)
    print Decimal(x.numerator) / Decimal(x.denominator)
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
