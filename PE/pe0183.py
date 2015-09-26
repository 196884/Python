from mpmath import *
import math

mp.dps = 30

def gcd(a, b):
    if a == b:
        return a
    if a < b:
        return gcd(b, a)
    if b == 0:
        return a
    return gcd(b, a%b)

def bestK(n):
    k0 = int(n / math.e)
    k1 = int(k0 + 1)
    v0 = (mpf(n) / mpf(k0)) ** k0
    v1 = (mpf(n) / mpf(k1)) ** k1
    if v0 > v1:
        return k0
    return k1

def contrib(n):
    k = bestK(n)
    g = gcd(n, k)
    d = k / g
    while d % 2 == 0:
        d /= 2
    while d % 5 == 0:
        d /= 5
    if d == 1:
        return -n
    return n

def solve():
    r = 0
    for n in range(5, 10001):
        r += contrib(n)
    return r
    
if __name__ == "__main__":
    result = solve()
    print "Result: %s" % result
