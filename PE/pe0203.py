def getExponents(n, primes):
    r = []
    for p in primes:
        e = 0
        pk = p
        while n % pk == 0:
            e += 1
            pk *= p
        r.append(e)
    return r

def multE(e1, e2):
    r = []
    for i, x in enumerate(e1):
        r.append(x + e2[i])
    return r

def divE(e1, e2):
    r = []
    for i, x in enumerate(e1):
        r.append(x - e2[i])
    return r

def expand(l, primes):
    r = 1
    for i, k in enumerate(l):
        r *= primes[i] ** k
    return r

def binomial(n, k, fl, primes):
    l = divE(fl[n], fl[k])
    l = divE(l, fl[n-k])
    for x in l:
        if x >= 2:
            return 0
    return expand(l, primes)

def solve():
    # Naive approach, doing arithmetic on representations as vectors of exponents of the first
    # few prime numbers
    primes = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47 ]
    np = len(primes)
    B = 50 
    factorials = [getExponents(1, primes), getExponents(1, primes)]
    for n in range(2, B+1):
        en = getExponents(n, primes)
        factorials.append(multE(en, factorials[-1]))
    s = set()
    for n in range(0, B+1):
        for k in range(0, n+1):
            s.add(binomial(n, k, factorials, primes))
    return sum(s)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
