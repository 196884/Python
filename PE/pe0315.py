B = 2 * 10 ** 7

protoSeg = [
    [0, 2, 3, 4, 5, 6],
    [4, 6],
    [0, 1, 2, 3, 6],
    [0, 1, 2, 4, 6],
    [1, 4, 5, 6],
    [0, 1, 2, 4, 5],
    [0, 1, 2, 3, 4, 5],
    [2, 4, 5, 6],
    [0, 1, 2, 3, 4, 5, 6],
    [0, 1, 2, 4, 5, 6],
]

def countSeg(n):
    r = 0
    while n > 0:
        if n % 2 == 1:
            r += 1
        n /= 2
    return r

def digitalRoot(n):
    r = 0
    while n > 0:
        r += n % 10
        n /= 10
    return r


segments = []
for l in protoSeg:
    segments.append(sum([2 ** i for i in l]))
nbSegments = [countSeg(k) for k in range(0, 2 ** 7)]

cacheAll = [(None, None) for n in range(0, B+1)]
cache1 = [None for n in range(0, B+1)]

def doFirst(n):
    if 0 == n:
        return 0
    cached = cache1[n]
    if cached != None:
        return cached
    r = doFirst(n / 10) + nbSegments[segments[n % 10]]
    cache1[n] = r
    return r

def doMaxTransition(n1, n2):
    """
    Assumes n1 >= n2
    """
    r = 0
    while n1 > 0:
        if n2 > 0:
            t  = segments[n1 % 10] ^ segments[n2 % 10]
            r += nbSegments[t]
        else:
            r += nbSegments[segments[n1 % 10]]
        n1 /= 10
        n2 /= 10
    return r

def doSeq(n, last):
    (cS, cM) = cacheAll[n]
    if cS != None:
        return (cS, cM)
    n2 = digitalRoot(n)
    if n2 == n:
        # Final one, we just need to switch off
        cacheAll[n] = (last, last)
        return (last, last)
    last2 = doFirst(n2)
    rS = last + last2
    rM = doMaxTransition(n, n2)
    (rS2, rM2) = doSeq(n2, last2)
    rS += rS2
    rM += rM2
    cacheAll[n] = (rS, rM)
    return (rS, rM)

def doAll(n):
    first = doFirst(n)
    (rS, rM) = doSeq(n, first)
    return (rS + first, rM + first)

def solve():
    primes = []
    isPrime = [True for n in range(0, B+1)]
    for n in range(2, B+1):
        if isPrime[n]:
            p = n
            if p > B / 2:
                primes.append(p)
            pk = 2 * p
            while pk <= B:
                isPrime[pk] = False
                pk += p

    rS = 0
    rM = 0
    for p in primes:
        (rS2, rM2) = doAll(p)
        rS += rS2
        rM += rM2
    return rS - rM

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
