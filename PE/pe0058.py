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

def solve():
    primes = primeSieve(1000000)
    nbPrimes = 0
    k        = 0
    total    = 1
    while True:
        k += 1
        # we investigate the 2k+1-sized square, adding the 4 new corners:
        if isPrime(2*k*(2*k-1)+1, primes):
            nbPrimes += 1
        if isPrime(2*k*(2*k+1)+1, primes):
            nbPrimes += 1
        if isPrime(2*k*2*k+1, primes):
            nbPrimes += 1
        # 4th diagonal is squares, so no primes there!
        total += 4
        #print "k: %d, p: %d, total: %d" % (k, nbPrimes, total)
        if 10 * nbPrimes < total:
            return 2*k+1

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
