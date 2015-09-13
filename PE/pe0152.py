import array
from fractions import Fraction
from decimal import *
from itertools import chain, combinations

getcontext().prec = 60

def gcd(a, b):
    if b > a:
        return gcd(b, a)
    if b == 0:
        return a
    return gcd(b, a%b)

def iSqrt(n):
    """
    Integral square root (by Newton iterations)
    """
    x    = 1
    xOld = 1
    while True:
        aux = ( x + ( n / x ) ) / 2
        if aux == x:
            return x
        if aux == xOld:
            return min(x, xOld)
        xOld = x
        x = aux

def primeSieve(n):
    """ 
    Returns all prime numbers <= n via Eratosthene's sieve
    """
    result = []
    sieve = array.array('i', (True for i in range(0, n+1)))
    for k in range(2, n+1):
        if sieve[k]:
            result.append(k)
            i = k * k
            while i <= n:
                sieve[i] = False
                i += k
    return result

def naiveFactorization(n):
    sqrt = iSqrt(n)
    primes = primeSieve(sqrt)
    result = []
    r = n
    for p in primes:
        q = 0
        while r % p == 0:
            q += 1
            r  = r / p
        if q > 0:
            result.append((p, q))
        if 1 == r:
            return result
    result.append((r, 1))
    return result

"""
Invariants: 
* current contains elements with indices < idx
* idx <= maxIdx
* current < target
"""
def aux(target, current, idx, details, maxIdx):
    if current >= target:
        raise NameError("unexpected")
    result = 0
    (a, b) = details[ idx ]
    # a is the current one being considered for inclusion
    # b is the sum of all the remaining ones (not including a)
    if idx < maxIdx:
        if current + b >= target:
            result += aux(target, current, idx+1, details, maxIdx)
        if current + a < target and current + a + b >= target:
            result += aux(target, current+a, idx+1, details, maxIdx)
    if current + a == target:
        result += 1
    return result

def isCandidate(x, primes):
    for p in primes:
        if p > 10 and x % p == 0:
            return False
    return True

def solve():
    n = 80
    primes = primeSieve(80)
    l = []
    lp = []
    for x in range(2, n+1):
        if isCandidate(x, primes):
            lp.append(x)
            l.append(x*x)
    print lp
    lcm = 13 * 13
    for x in l:
        g    = gcd(lcm, x)
        lcm *= x / g
    l2 = [ lcm / 144 ] # This is for the special '13' case...
    for x in l:
        l2.append( lcm / x )
    l2.sort()
    l2 = list( reversed( l2 ) )
    print l2
    t = lcm / 2
    details = []
    sumSoFar = 0
    sumAll = sum(l2)
    for x in l2:
        sumSoFar += x
        details.append((x, sumAll - sumSoFar))
        f = Fraction(x, lcm)
        print f
    print details
    result = aux( t, 0, 0, details, len(details)-1)
    return result
    

"""
Using this sieve, one checks that numerators cannot contain prime factors >= 11,
with a single exception: 13 (in which case it must contain:
1/13^2 + 1 / (3 * 13^2) + 1 / (4 * 13)^2

So we use the rest of the possible denominators (we actually do two cases, including
or excluding the 13 factors above
"""
def sieveFactors():
    pl = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31 ]
    d  = dict()
    fl = []
    for n in range(1, 8):
        fl.append( Fraction(1, n*n) )
    c = chain.from_iterable( combinations(fl, r) for r in range( len(fl)+1 ) )
    sc = set(c)
    for x in sc:
        xl = list(x)
        sl = sum(xl)
        sln = sl.numerator
        for p in pl:
            if sln % (p*p) == 0:
                print "Match for p=%d" % p
                print xl
    print d

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
