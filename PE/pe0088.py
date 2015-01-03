def factorsPow(p, k, jMax):
    # Generates all the factorizations of p^k where each factor is <= p^jMax
    if 0 == k:
        return [ [] ]
    r = []
    jMax = min(k, jMax)
    pj = p
    for j in range(1, jMax+1):
        auxL = factorsPow(p, k-j, min(j, jMax))
        for aux in auxL:
            r.append(aux + [pj])
        pj *= p
    return r

def rmDup(l):
    s = set()
    for x in l:
        s.add(tuple(x))
    sl = list(s)
    return [list(x) for x in sl]
 
def factorsAux2(l, p, k):
    if len(l) == 0:
        return factorsPow(p, k, k)
    if k == 0:
        return [l]

    r = []
    lh = l[-1]
    lt = l[:-1]
    pj = 1
    for j in range(0, k+1):
        auxLs = factorsAux2(lt, p, k-j)
        for auxL in auxLs:
            aux = auxL + [ lh * pj ]
            aux.sort()
            r.append(aux)
        pj *= p
    return rmDup(r)

def factorsAux1(l, p, k):
    r = []
    for x in l:
        aux = factorsAux2(x, p, k)
        r += aux
    return r
  
def solve():
    # Could be much faster and cleaner!
    B = 12200
    pInfo = [ (1, 1, 1) for i in range(0, B+1) ]
    factorizations = [[], [[]]]
    for n in range(2, B+1):
        (p, k, pk) = pInfo[n]
        if 1 == p:
            # Case where n is prime
            p = n
            k = 1
            pk = p
            while pk <= B:
                pkm = pk
                while pkm <= B:
                    pInfo[pkm] = (p, k, pk)
                    pkm += pk
                k += 1
                pk *= p
            (p, k, pk) = (p, 1, p)
        factorizations.append(factorsAux1(factorizations[n/pk], p, k))
        nb = len(factorizations[-1])
    bestJ = dict()
    for n in range(2, B+1):
        facts = factorizations[n]
        for f in facts:
            s = sum(f)
            # if n >= s, then by adding n-s '1's on each side, we get n
            if n >= s:
                j = len(f) + n - s
                if bestJ.get(j, 10**10) > n:
                    bestJ[j] = n
    s = set()
    for j in range(2, 12001):
        s.add(bestJ[j])
    return sum(s)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
