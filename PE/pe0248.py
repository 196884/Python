import array

def gcd(a, b):
    if a == b:
        return a
    if a < b:
        return gcd(b, a)
    if b == 0:
        return a
    return gcd(b, a%b)

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
    for p in primes:
        if n % p == 0:
            return n == p
        if p > n:
            return True
    return True

def genFactorsL(l):
    r = [ [] ]
    for (p, k) in l:
        rb = []
        for rl in r:
            for kk in range(0, k+1):
                rlb = list(rl)
                rlb.append((p, kk))
                rb.append(rlb)
        r = rb
    return rb

def genFactors(l):
    r = [1]
    a = 1
    for (p, k) in l:
        rb = []
        ppow = 1
        for kk in range(0, k+1):
            for x in r:
                rb.append(x * ppow)
            ppow *= p
        r = rb
        a *= p ** k
    return (a, r)

def fullFact(l):
    d = dict()
    l = genFactorsL(l)
    for ll in l:
        (k, v) = genFactors(ll)
        d[k] = v
    return d

# Given a number n, and a list of its factors,
# tries to find a prime p and an integer k such
# that
# phi(p^k) = n
def inversePhi(n, nFactors, primes):
    r = []
    for f in nFactors:
        p = f+1
        if isPrime(p, primes):
            m = f
            k = 1
            while m < n:
                m *= p
                k += 1
            if m == n:
                r.append(p ** k)
    return r

def subBasis(basis, target):
    r = dict()
    for k, v in basis.iteritems():
        if target % k == 0:
            r[k] = v
    return r

def maxFactor(n, factors):
    for f in factors:
        if n % f == 0:
            return f
    return 1

def genPs(pCurr, phiTarget, basis, phiPs, allNs):
    if phiTarget == 1:
        allNs.add(pCurr)
        if pCurr % 2 == 1:
            allNs.add(2 * pCurr)
        return allNs
    p = maxFactor(phiTarget, phiPs)
    bp = basis[p]
    for phiFactor, pList in bp.iteritems():
        if phiTarget % phiFactor == 0:
            for ppow in pList:
                if gcd(pCurr, ppow) == 1:
                    allNs = genPs(pCurr * ppow, phiTarget / phiFactor, basis, phiPs, allNs)
    return allNs

def solve():
    # 13! factorizes as:
    phi13 = 13*12*11*10*9*8*7*6*5*4*3*2
    phiFact = [(2, 10), (3, 5), (5, 2), (7, 1), (11, 1), (13, 1)]
    phiPs = []
    for (p, k) in reversed(phiFact):
        phiPs.append(p)
    primes = primeSieve(iSqrt(phi13))
    ff = fullFact(phiFact)
    basis = dict()
    for p in phiPs:
        basis[p] = dict()
    for n, nFactors in ff.iteritems():
        ip = inversePhi(n, nFactors, primes)
        if len(ip) > 0 and n > 1:
            p = maxFactor(n, phiPs)
            basis[p][n] = ip
    print "Basis generated..."
    allNs = set()
    allNs = genPs(1, phi13, basis, phiPs, allNs)
    l     = list(allNs)
    l.sort()
    return l[149999]

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
