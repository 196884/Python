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

def primeSieve(b):
    sieve = [ True for i in range(0, b+1)]
    maxFactor = iSqrt(b)
    for n in range(2, maxFactor+1):
        if sieve[n]:
            # n is prime
            nk = 2 * n
            while nk <= b:
                sieve[nk] = False
                nk += n
    result = []
    for n in range(2, b+1):
        if sieve[n]:
            result.append(n)
    return result

def genMasks(n):
    # Generates all possible masks of n digits:
    l = [ 0 ]
    for i in range(0, n):
        lNew = []
        for m in l:
            lNew.append(10 * m + 1)
            lNew.append(10 * m)
        l = list(lNew)
    return l

def solve():
    # We look for a solution below 1000000, hopefully that should work
    b = 1000000
    primes = primeSieve(b)
    primeSet = set(primes)
    masks = genMasks(5)
    masks = masks[:-1]
    masks = list(reversed(masks))
    for p in primes:
        n     = p
        masks = [0 for i in range(0, 10)]
        # l[d] should be the mask for digit d:
        p10   = 1
        while n > 0:
            masks[n%10] += p10
            n /= 10
            p10 *= 10
        for d in range(0, 10):
            mask = masks[d]
            if mask > 0:
                pb = p - d * mask
                test = 0
                for i in range(0, 10):
                    pi = pb + i * mask
                    if pi >= p and pi in primeSet:
                        test += 1
                if test >= 8:
                    return p

    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

