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

def seriesMult(s1, s2):
    n = len(s1)
    r = [0 for i in range(0, n)]
    for i in range(0, n):
        s1i = s1[i]
        for j in range(0, n-i):
            r[i+j] += s1i * s2[j]
    return r

def seriesMultP(s1, p):
    # multiplies s1 by 1/(1-x^p):
    r  = list(s1)
    n  = len(s1)
    pk = p
    while pk < n:
        for i in range(0, n-pk):
            r[i+pk] += s1[i]
        pk += p
    return r

def solve():
    # computing successively the 1/(1-x^p) for p prime...
    primes = primeSieve(10000)
    l = [0 for i in range(0, 200)]
    l[0] = 1
    for p in primes:
        l = seriesMultP(l, p)
        for n in range(0, p):
            if l[n] >= 5000:
                return n

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
