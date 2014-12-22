# We're using the fact that there are only 11
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
    primes  = primeSieve(100000)
    digits  = [1, 2, 3, 5, 7, 9]
    result  = 0
    nbFound = 0
    setL    = set([3, 7])
    setR    = set([2, 3, 5, 7])
    pow10   = 1
    while True:
        pow10 *= 10
        setLCurr = set()
        setRCurr = set()
        for l in setL:
            for p in digits:
                x = pow10 * p + l
                if isPrime(x, primes):
                    setLCurr.add(x)
        for r in setR:
            for p in digits:
                x = p + 10 * r
                if isPrime(x, primes):
                    setRCurr.add(x)
        setL = set(setLCurr)
        setR = set(setRCurr)
        s = setL.intersection(setR)
        for x in s:
            result += x
            nbFound += 1
            if nbFound == 11:
                return result

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
