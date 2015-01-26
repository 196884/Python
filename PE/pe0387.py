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

def genHarshad(l, k):
    if k == 1:
        return l
    ll = []
    for (p, s) in l:
        for d in range(0, 10):
            p2 = 10 * p + d
            s2 = s + d
            if p2 % s2 == 0:
                ll.append((p2, s2))
    return genHarshad(ll, k-1)

def testPrime(n, primes):
    for p in primes:
        if n % p == 0:
            return n == p
    return True

def solve():
    l = [(i, i) for i in range(1, 10)]
    K = 13 
    lll = []
    for k in range(2, K+1):
        ll = genHarshad(l, k)
        for x in ll:
            lll.append(x)
    l = lll
    B = 10 ** 7
    primes = []
    isPrime = [True for i in range(0, B+1)]
    for n in range(2, B+1):
        if isPrime[n]:
            p = n
            primes.append(p)
            pk = 2 * p
            while pk <= B:
                isPrime[pk] = False
                pk += p
    r = 0
    for (n, sd) in l:
        if testPrime(n / sd, primes):
            for d in [1, 3, 7, 9]:
                n2 = 10 * n + d
                if testPrime(n2, primes):
                    r += n2
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
