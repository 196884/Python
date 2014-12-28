def iterFarey(l, bound):
    # b is the upper bound
    r = [(0, 1)]
    prev = (0, 1)
    for (a, b) in l[1:]:
        aa = a + prev[0]
        bb = b + prev[1]
        if bb <= bound:
            r.append((aa, bb))
        r.append((a, b))
        prev = (a, b)
    return r

def iterFareyFast(x, bound):
    (n, l) = x
    # n is the separate count
    # l is a list of lists...
    r = []
    for ll in l:
        if len(ll) == 1:
            n += 1
        else:
            rr = []
            prev = None
            for (a, b) in ll:
                if prev == None:
                    rr.append((a, b))
                    prev = (a, b)
                else:
                    aa = a+prev[0]
                    bb = b+prev[1]
                    if bb <= bound:
                        rr.append((aa, bb))
                        rr.append((a, b))
                        prev = (a, b)
                    else:
                        r.append(rr)
                        rr = [(a, b)]
                        prev = (a, b)
            r.append(rr)
    return (n, r)

def solve():
    # Two phases:
    # 1. We determine the index of 1/3 in the Farey sequence (by some fast-ish Stern-Brocot tree construction/pruning)
    # 2. We determine the size of the entire Farey sequence (as per the previous problem), which directly gives the index
    #    of 1/2 (by symmetry)
    # Note that 1. gets progressively faster due to the pruning
    n = 12000
    l = [(0, 1), (1, 3)]
    x = (0, [l])
    k = 0
    done = False
    while not done:
        x = iterFareyFast(x, n)
        k += 1
        done = len(x[1]) == 0
    F_3 = x[0] - 1
        
    # this is directly the sum of the phi(m), for m from 2 to 1000000
    # we first sieve...
    b = n + 1
    isPrime = [True for i in range(0, b)]
    hFactor = [None for i in range(0, b)]
    # hFactor[n] will contain (p, p^k), where:
    # * p is the largest prime factor of n
    # * p^k is the highest power of p dividing n
    for n in range(2, b):
        if isPrime[n]:
            pk = n
            while pk < b:
                mpk = pk
                while mpk < b:
                    isPrime[mpk] = False
                    hFactor[mpk] = (n, pk)
                    mpk += pk
                pk *= n
    phi = [1 for i in range(0, b)]
    F_1 = 0
    for i in range(2, b):
        (p, pk) = hFactor[i]
        aux = (pk / p) * (p-1) * phi[i / pk]
        phi[i] = aux
        F_1 += aux
    F_2 = ( F_1 - 1 ) / 2
    return (F_1 - 1) / 2 - F_3

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
