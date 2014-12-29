import math as math
import array

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

def evalF(l):
    if len(l) == 0:
        return 1
    n = l[-1]
    aux = evalF(l[:-1])
    return 1 + n + (2 * n + 1) * (aux - 1)

def evalN(l, primes):
    r = 1
    for i, k in enumerate(l):
        r *= primes[i] ** k
    return r

def solve():
    # we use our formula from pe0108, but we know that the result is
    # going to be smooth, so we focus on these...
    primes = primeSieve(1000)
    b = 4000000

    # First, we get a bound (by checking what happens if we stick
    # with exponents of 1...)
    l = []
    v = evalF(l)
    while v < b:
        l.append(1)
        v = evalF(l)
    nbPrimes = len(l)
    primes = primes[:nbPrimes]
    # We do an exhaustive search on the first few exponents, assuming they will be
    # in our guessed bounds:
    bounds = [8, 7, 6, 5, 4, 3, 2, 1]
    # Below was found after some exhaustive search, and then some checks to make sure
    bestL = [3, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1]
    return evalN(bestL, primes)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
