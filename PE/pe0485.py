import array

def getMax(l, k, lastIdx):
    print "getMax - %d" % lastIdx
    r = 0
    for i in range(0, k):
        r = max(r, l[lastIdx - i])
    return r

def solve():
    N = 10**8
    k = 10**5
    ks = array.array('i', (0 for i in range(0, N+1)))
    pks = array.array('i', (0 for i in range(0, N+1)))
    nbDivs = array.array('i', (0 for i in range(0, N+1)))
    nbDivs[1] = 1
    for n in range(2, k+1):
        print n
        pk = pks[n]
        if pk == 0:
            p = n
            pk = p
            kk = 1
            while pk <= N:
                mpk = pk
                while mpk <= N:
                    ks[mpk] = kk
                    pks[mpk] = pk
                    mpk += pk
                pk *= p
                kk += 1
            nbd = 2
        else:
            nbd = (ks[n] + 1) * nbDivs[n / pks[n]]
        nbDivs[n] = nbd
    currMax = getMax(nbDivs, k, k)
    r = currMax
    for n in range(k+1, N+1):
        pk = pks[n]
        if pk == 0:
            p = n
            pk = p
            kk = 1
            while pk <= N:
                mpk = pk
                while mpk <= N:
                    ks[mpk] = kk
                    pks[mpk] = pk
                    mpk += pk
                pk *= p
                kk += 1
            nbd = 2
        else:
            nbd = (ks[n] + 1) * nbDivs[n / pks[n]]
        nbDivs[n] = nbd
        if nbd > currMax:
            r += nbd
            currMax = nbd
        else:
            if nbDivs[n-k] < currMax:
                r += currMax
            else:
                currMax = getMax(nbDivs, k, n)
                r += currMax
    return r

if __name__ == "__main__":
    # Naive, and not super efficient for the max, but good enough given the number of scans seen
    result = solve()
    print "Result: %d" % result
