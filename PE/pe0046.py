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

def solve():
    primeList = primeSieve(10000)
    primeSet = set(primeList)
    k = 1
    while True:
        n = 2 * k + 1
        k += 1
        a = 0
        a2 = 0
        while a2 < n and (n - 2 * a2) not in primeSet:
            a2 += 2 * a + 1
            a += 1
        if a2 >= n:
            return n

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
