def solve():
    m = 10 ** 8
    n = 10 ** 12
    middles = [ (0,3), (0,7), (1,4), (2,3), (3,0), (3,2), (3,5), (3,6), (4,1), (5,3), (5,7), (7,3), (6,5), (6,0), (6,6), (7,7) ]
    starts  = [ 0, 2, 5, 6 ]
    ends    = [ 3, 6 ]
    total   = []
    for s in starts:
        for e in ends:
            total.append((s, e))
    
    # We build the basis (powers of 2)
    d = dict()
    for x in middles:
        d[x] = 1
    l = [d]
    while 2 ** len(l) <= n-2:
        d = dict()
        for (a1, b1), v1 in l[-1].iteritems():
            for (a2, b2), v2 in l[-1].iteritems():
                if b1 == a2:
                    ab = (a1, b2)
                    nb = d.get(ab, 0)
                    d[ab] = (nb + v1 * v2) % m
        l.append(d)

    # we now assemble the above to get a length of n-2:
    d = dict()
    for (a, b) in middles:
        d[(a, a)] = 1 # to have generic code below

    aux = n-2
    idx = 0
    while aux > 0:
        if aux % 2 == 1:
            da = dict()
            d1 = d
            d2 = l[idx]
            for (a1, b1), v1 in d1.iteritems():
                for (a2, b2), v2 in d2.iteritems():
                    if b1 == a2:
                        ab = (a1, b2)
                        nb = da.get(ab, 0)
                        da[ab] = (nb + v1 * v2) % m
            d = da
        aux /= 2
        idx += 1

    r = 0
    for ab in total:
        r = (r + d.get(ab, 0)) % m

    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
