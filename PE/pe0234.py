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

def sumInRange(a, b):
    # returns the sum of n for which a <= n <= b:
    r  = b * (b+1) / 2
    r -= a * (a-1) / 2
    return r

def solve():
    """
    We can start by looking at the pairs of consecutive primes
    p1, p2
    where p1 ** 2 <= B (999966663333)
    We then need to sum the multiples of p1, and then of p2 (but not of both):
    """
    M = 1000
    M = 999966663333
    sqrtM = iSqrt(M)
    B = sqrtM + 1000 
    primes = []
    isPrime = [ True for n in range(0, B) ] # safety margin: we need one extra prime!
    for n in range(2, B):
        if isPrime[n]:
            p = n
            primes.append(p)
            pk = 2 * p
            while pk < B:
                isPrime[pk] = False
                pk += p
    i = 0
    p1 = 2
    r = 0
    count = 0
    while p1 * p1 <= M:
        p2 = primes[i+1]
        l1 = p1 + 1
        u1 = min(M / p1, (p2 * p2) / p1)
        n1 = sumInRange(l1, u1)
        r += p1 * n1
        l2 = (p1 * p1) / p2 + 1
        u2 = min(p2 - 1, M / p2)
        n2 = sumInRange(l2, u2)
        r += p2 * n2
        i += 1
        if p1 * p2 <= M:
            r -= 2 * p1 * p2
        p1 = primes[i]
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
