# The goal is to return the largest prime factor of
# 600851475143

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

def solve():
    l = naiveFactorization(600851475143)
    (r, _) = l[-1]
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
