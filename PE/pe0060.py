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

def isPrime(n, primes):
    if n == 1:
        return False
    for p in primes:
        if n % p == 0:
            return n == p
        if p * p > n:
            return True
    return True

def canConcat(p1, p2, primes):
    p12 = int(str(p1) + str(p2))
    if not isPrime(p12, primes):
        return False
    p21 = int(str(p2) + str(p1))
    return isPrime(p21, primes)

def solve():
    # Naive, but painfully slow!!! (I don't care about optimizing this one, though...)
    primes = primeSieve(10000)
    primeSet = set(primes)
    pMax = primes[-1]
    pBound = 10000

    l = []

    for p1 in primes:
        print p1
        for p2 in primes:
            if p2 > p1:
                if canConcat(p1, p2, primes):
                    for p3 in primes:
                        if p3 > p2:
                            if canConcat(p1, p3, primes) and canConcat(p2, p3, primes):
                                for p4 in primes:
                                    if p4 > p3:
                                        if canConcat(p1, p4, primes) and canConcat(p2, p4, primes) and canConcat(p3, p4, primes):
                                            for p5 in primes:
                                                if p5 > p4:
                                                    if canConcat(p1, p5, primes) and canConcat(p2, p5, primes) and canConcat(p3, p5, primes) and canConcat(p4, p5, primes):
                                                        s = p1+p2+p3+p4+p5
                                                        l.append(s)
    return min(l)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
