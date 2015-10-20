import array

def genDivs(n, aP, aPk, aK):
    r = [1]
    while n > 1:
        l     = []
        pK    = 1
        p     = aP[n]
        pKMax = aPk[n]
        while pK <= pKMax:
            for er in r:
                l.append(pK * er)
            pK *= p
        n /= pKMax
        r = l
    return r

def sieve(B):
    r = 0
    sL = set()
    sH = set()
    # generates 3 arrays: aP, aPk, aK: aPk[i] = aP[i] ^ aK[i] is the largest prime power of i
    aP  = array.array('i', (0 for i in range(0, B+1)))
    print "aP allocated"
    aPk = array.array('i', (0 for i in range(0, B+1)))
    print "aPk allocated"
    aK  = array.array('i', (0 for i in range(0, B+1)))
    print "aK allocated"
    aNbDivs = array.array('i', (0 for i in range(0, B+1)))
    aNbDivs[1] = 1
    for n in range(2, B+1):
        if aP[n] == 0:
            # n is prime
            p = n
            k  = 1
            pK = p
            while pK <= B:
                pKmul = pK
                while pKmul <= B:
                    aP[pKmul]  = p
                    aK[pKmul]  = k
                    aPk[pKmul] = pK
                    pKmul     += pK
                pK *= p
                k  += 1
            aNbDivs[n] = 2
        else:
            # n is composite...
            nbDivs     = (1 + aK[n]) * aNbDivs[n / aPk[n]]
            aNbDivs[n] = nbDivs
            if n % 2 == 0 and nbDivs > 400:
                r += 1
                print (r, n, nbDivs)
                divs = genDivs(n, aP, aPk, aK)
                for d in divs:
                    sL.add(min(d, n/d))
                    sH.add(max(d, n/d))
                print ("lengths", len(sL), len(sH))
                #print genDivs(n, aP, aPk, aK)
    print r
    l = list(sL)
    l.sort()
    print l
    l = list(sH)
    l.sort()
    print l
    return (aP, aK, aPk)

# To check compositions fast:
# we want to check positive numbers are *not* contained in
# aZZ + bZZ, for a given pair (a, b).
# WLOG, we can assume that gcd(a, b) = 1
# We assume that x.a - y.b = 1 (x and y > 0)

def checkCompositionOdd(k, B):
    # B is the bound on the size...
    r = array.array('b', (False for i in range(0, B+1)))
    #r = [False for i in range(B+1)]
    a = k - 1
    b = k + 1
    aMul = 0
    while aMul <= B:
        s = aMul
        while s <= B:
            r[s] = True
            s += b
        aMul += a 
    return r

def checkCompositionEven(k, B):
    r = array.array('b', (False for i in range(0, B+1)))
    #r = [False for i in range(B+1)]
    r[1] = True
    a = k-2
    b = k
    sa = -1
    while sa <= B:
        s = sa
        if s < 0:
            s += b + 1
        while s <= B:
            r[s] = True
            r[min(B, s+1)] = True
            r[min(B, s+2)] = True
            s += b + 1
        sa += a + 1
    return r

def solve():
    n = 100000000
    (aP, aK, aPk) = sieve(n)
    return 0
    B = 20000
    c = dict()
    for k in range(3, B+1):
        if k % 2 == 0:
            d = checkCompositionEven(k, B)
        else:
            d = checkCompositionOdd(k, B)
        for x in range(k, B+1):
            if not d[x]:
                v = c.get(k * x, 0)
                c[k * x] = v + 1
        if k < 100 or k % 100 == 0:
            print "Done with k[%d]" % k
    m = 0
    for k, v in c.iteritems():
        m = max(m, v)
        if v == 200:
            print k
    print "Max found[%d]" % m
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
