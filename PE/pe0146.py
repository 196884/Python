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

def arePrime(l, primes):
    for p in primes:
        for n in l:
            if (p < n) and (n % p == 0):
                return False
    return True

def isPrime(n, primes):
    for p in primes:
        if p >= n:
            return True
        if n % p == 0:
            return False
    return True

def check(n, l, primes):
    if not arePrime(l, primes):
        return False
    if isPrime(n**2 + 19, primes) or isPrime(n**2+21, primes):
        return False
    return True

def solve():
    # by looking at congruences mod 2 and mod 5, one checks that n has to
    # be divisible by 10, and that the only remaining numbers that could be
    # prime are n^2+19 and n^2+21

    # Bruteforcing from that:
    b = 150000000
    primes = primeSieve(b)
    print "Generated primes (%d)" % len(primes)

    l = [1, 3, 7, 9, 13, 27]
    r = 0
    n = 0
    while n < b:
        l = [ x + 20 * n + 100 for x in l ]
        n += 10
        if check(n, l, primes):
            r += n
            print "Found %d" % n
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
