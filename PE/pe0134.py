def euclid(a, b):
    """
    Returns a triple (g, m, n) such that
    g = m.a + n.b
    where g is the gcd of a and b
    """
    if a == b:
        return (a, 1, 0)
    if b > a:
        (g, m, n) = euclid(b, a)
        return (g, n, m)
    rpp = a
    rp  = b
    mpp = 1
    mp  = 0
    npp = 0
    np  = 1
    while rp > 0:
        q = rpp / rp
        r = rpp % rp
        m = mpp - q * mp
        n = npp - q * np
        rpp = rp
        rp  = r
        mpp = mp
        mp  = m
        npp = np
        np  = n
    return (rpp, mpp, npp)

def log10(n):
    r = 1
    while n > 0:
        r *= 10
        n /= 10
    return r

def powMod(a, b, m):
    a2k    = a # a^(2^k)
    result = 1
    while b > 0:
        if b % 2 == 1:
            result = (result * a2k) % m
        a2k = (a2k * a2k) % m
        b /= 2
    return result

def check(p):
    l = powMod(10, 10, p)
    h = powMod(10, 100, p)
    while 1 != l and l != h:
        l = powMod(l, 10, p)
        h = powMod(h, 100, p)
    return 1 == l

def solve():
    B = 10 ** 6 + 1000
    primes = []
    isPrime = [True for n in range(0, B+1)]
    for n in range(2, B+1):
        if isPrime[n]:
            p = n
            primes.append(p)
            pk = 2 * p
            while pk <= B:
                isPrime[pk] = False
                pk += p
    r = 0
    for i, p1 in enumerate(primes):
        if p1 > 10 ** 6:
            return r
        if p1 >= 5:
            k1 = log10(p1)
            p2 = primes[i+1]
            (_, a, _) = euclid(p2, k1)
            a = (a * p1) % k1
            r += a * p2
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
