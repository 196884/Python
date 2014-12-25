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
    b = 50000000
    pMax = iSqrt(b)
    primes = primeSieve(pMax)
    p2s = [ p ** 2 for p in primes ]
    p3b = [ p ** 3 for p in primes ]
    p4b = [ p ** 4 for p in primes ]
    p3s = [ x for x in p3b if x < b ]
    p4s = [ x for x in p4b if x < b ]
    cache = set()
    # There are 908 primes in primes
    for p4 in p4s:
        for p3 in p3s:
            for p2 in p2s:
                s = p2 + p3 + p4
                if s < b:
                    cache.add(s)
    return len(cache)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
