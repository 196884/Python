import itertools as it

def isPrime(n, primes):
    for p in primes:
        if p * p > n:
            return True
        if n % p == 0:
            return False

def listToInt(l):
    r = 0
    for x in reversed(l):
        r = 10 * r + x
    return r

def mergeSets(s1, s2):
    # s1 and s2 represent non-empty sets of digits
    # the function returns 0 if the intersection is non-empty,
    # the union otherwise
    r  = 0
    p2 = 1
    while s1 > 0 or s2 > 0:
        d1 = s1 % 2
        d2 = s2 % 2
        if d1 * d2 > 0:
            return 0
        r += p2 * (d1 + d2)
        p2 *= 2
        s1 /= 2
        s2 /= 2
    return r

def getSet(n):
    # returns the digit-set of n,
    # or 0 if n contains a 0 digit or twice the same digit
    value = [ 2 ** i for i in range(0, 10)]
    value[0] = 0
    r = 0
    k = 0
    while n > 0:
        d = n % 10
        if value[d] == 0:
            return (0, 0)
        r += value[d]
        k += 1
        value[d] = 0
        n /= 10
    return (k, r)

def lToInt(l):
    r = 0
    for x in l:
        r = 10 * r + x
    return r

def setSize(s):
    r = 0
    while s > 0:
        r += s % 2
        s /= 2
    return r

def setToList(s):
    r = []
    k = 0
    while s > 0:
        if s % 2 == 1:
            r.append(k)
        s /= 2
        k += 1
    return r

def solve():
    primes = []
    # keyed by size and then set of digits
    panPrimes = [ dict() for i in range(0, 10) ]
    nb = 6
    b = 10 ** nb 
    sieve = [True for i in range(0, b)]
    for n in range(2, b):
        if sieve[n]:
            # n is prime
            p = n
            (aa, bb) = getSet(p)
            if aa > 0:
                da = panPrimes[aa]
                v = da.get(bb, 0)
                da[bb] = v + 1
            primes.append(p)
            mp = p
            while mp < b:
                sieve[mp] = False
                mp += p

    # At this point, the primes have been generated up to the specified size
    allDigits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for nb2 in range(nb+1, 9):
        for c in it.combinations(allDigits, nb2):
            s = sum([2 ** i for i in c])
            for cc in it.permutations(c):
                n = lToInt(cc)
                if isPrime(n, primes):
                    dnb2 = panPrimes[nb2]
                    v = dnb2.get(s, 0)
                    dnb2[s] = v + 1

    # Now we combine them and count, but we need to prevent counting twice
    panSets = [ dict() for i in range(0, 10) ]
    panSets[0][0] = 1
    for k1, d1 in enumerate(panPrimes):
        for kx, nx in d1.iteritems():
            for k2, d2 in enumerate(panSets):
                if k1 + k2 < 10:
                    k3 = k1 + k2
                    d3 = panSets[k3]
                    for ky, ny in d2.iteritems():
                        kz = mergeSets(kx, ky)
                        if kz > 0:
                            v = d3.get(kz, 0)
                            d3[kz] = v + nx * ny
    return panSets[9][1022]

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
