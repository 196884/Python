import itertools as it

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

def isPrime(n, primes):
    for p in primes:
        if p * p > n:
            return True
        if n % p == 0:
            return False

def primesWithPattern(n, k, d, primes):
    mults = [10 ** i for i in range(0, n)]
    digits = range(0, n)
    allDigits = set(digits)
    b = 10 ** (n-k)
    r = 0
    for kDigits in it.combinations(digits, k):
        extraDigits = allDigits.difference(set(kDigits))
        ppBase = 0
        for i in kDigits:
            ppBase += d * 10 ** i
        for i in range(0, b):
            aux = i
            pp = ppBase
            for e in extraDigits:
                pp += (aux % 10) * 10 ** e
                aux /= 10
            if pp >= 10 ** (n-1) and isPrime(pp, primes):
                r += pp
    return r

def solve():
    primes = []
    b = 10 ** 6
    sieve = [True for i in range(0, b)]
    for n in range(2, b):
        if sieve[n]:
            # n is prime
            p = n
            primes.append(p)
            mp = p
            while mp < b:
                sieve[mp] = False
                mp += p
    r = 0
    n =10 
    for d in range(0, 10):
        k = n+1
        x = 0
        while x == 0:
            k -= 1
            x = primesWithPattern(n, k, d, primes)
        r += x
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
