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

def primeSieve(b):
    sieve = [ True for i in range(0, b+1)]
    maxFactor = iSqrt(b)
    for n in range(2, maxFactor+1):
        if sieve[n]:
            # n is prime
            nk = 2 * n
            while nk <= b:
                sieve[nk] = False
                nk += n
    result = []
    for n in range(2, b+1):
        if sieve[n]:
            result.append(n)
    return result

def solve():
    # the sum of the first 547 primes is above 1000000, so we use this as a bound
    # since there are 78498 primes below 1000000, we can bruteforce it
    b = 1000000
    primes = primeSieve(b)
    np = len(primes)
    primeSet = set(primes)
    l = 547
    while True:
        # trying to find a sequence of length l that works (we could optimize for
        # even/odd, but we don't care that much)
        currSum = 0
        for n in range(0, l):
            currSum += primes[n]
        iMax = l - 1
        while iMax < np:
            if currSum in primeSet:
                return currSum
            iMax += 1
            if iMax < np:
                currSum += primes[iMax] - primes[iMax-l]
        l -= 1

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

