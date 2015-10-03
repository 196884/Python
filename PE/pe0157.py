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

def sieve(n):
    # returns (primes, pks) where:
    # * primes is the list of all prime numbers in [2, n]
    # * pks[n] = (p, k) to signify that p is the largest prime dividing n, and p^k its largest power dividing n
    primes = []
    pks = [(1, 0) for i in range(n+1)]
    for k in range(2, n+1):
        if pks[k][0] == 1:
            # k is prime
            p = k
            primes.append(p)
            # invariant: ppow = p^m
            ppow = p
            m = 1
            while ppow <= n:
                ppowMul = ppow
                while ppowMul <= n:
                    pks[ppowMul] = (p, m)
                    ppowMul += ppow
                ppow *= p
                m += 1
    return (primes, pks)

def countFactorsP(n, p):
    r = 1
    while n % p == 0:
        r += 1
        n /= p
    return (r, n)

def countFactors(n, primes):
    r = 1
    for p in primes:
        (k, n) = countFactorsP(n, p)
        r *= k
        if n == 1:
            return r
    r *= 2
    return r

def solve():
    B = 2 * 10 ** 9
    sqrtB = iSqrt(B)
    (primes, pks) = sieve(5*sqrtB)
    r = 0
    for n in range(1, 10):
        for k1 in range(1, n+1):
            alpha = 2**k1
            for k2 in range(1, n+1):
                beta = 5**k2
                r += countFactors( 2**(n-k1) * 5**(n-k2) * (alpha + beta), primes )
        for k1 in range(0, n+1):
            for k2 in range(0, n+1):
                beta = 2**k1 * 5**k2
                r += countFactors( 2**(n-k1) * 5**(n-k2) * (1 + beta), primes )
    return r
    
if __name__ == "__main__":
    result = solve()
    print result
