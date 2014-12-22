import array

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

def getDigits(n):
    r = []
    while n > 0:
        r.append(n % 10)
        n /= 10
    r.sort()
    return r

def solve():
    primes = primeSieve(10000)
    primeSet = dict()
    r = 0
    for p in primes:
        if p >= 1000:
            primeSet[p] = getDigits(p)
    for pi, pid in primeSet.iteritems():
        for pj, pjd in primeSet.iteritems():
            if pi < pj and pid == pjd:
                pk = (pi + pj) / 2
                pkd = primeSet.get(pk, [])
                if pkd == pid:
                    c = 100000000 * pi + 10000 * pk + pj
                    if c != 148748178147:
                        return c
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
