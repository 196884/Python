def genCallList(n):
    r = [ (100003 - 200003 * k + 300007 * k ** 3) % 1000000 for k in range(1, 56) ]
    for k in range(55, n):
        c = (r[-24] + r[-55]) % 1000000
        r.append(c)
    return r

def solve():
    callList = genCallList(5000000)
    setIdx = [-1 for n in range(0, 10 ** 6)]
    sets   = dict() # set idx -> set
    nextSetIdx = 0
    pmNb       = 524287
    pmSetSize  = 0
    pmSetIdx   = -1
    r          = 0
    for k in range(0, 5000000):
        c1 = callList[2 * k]
        c2 = callList[2 * k + 1]
        if c1 != c2:
            r += 1
            i1 = setIdx[c1]
            i2 = setIdx[c2]
            if i1 < 0:
                if i2 < 0:
                    # Introducing a new set:
                    s12 = set([c1, c2])
                    i12 = nextSetIdx
                    nextSetIdx += 1
                    if c1 == pmNb or c2 == pmNb:
                        pmSetIdx = i12
                        pmSetSize = 2
                    sets[i12] = s12
                    setIdx[c1] = i12
                    setIdx[c2] = i12
                else:
                    # We add c1 to the set to which c2 belongs:
                    setIdx[c1] = i2
                    sets[i2].add(c1)
                    if c1 == pmNb:
                        pmSetIdx = i2
                    if pmNb in sets[i2]:
                        pmSetSize = len(sets[i2])
            else:
                if i2 < 0:
                    # We add c2 to the set to which c1 belongs:
                    setIdx[c2] = i1
                    sets[i1].add(c2)
                    if c2 == pmNb:
                        pmSetIdx = i1
                    if pmNb in sets[i1]:
                        pmSetSize = len(sets[i1])
                elif i1 != i2:
                    nb1 = len(sets[i1])
                    nb2 = len(sets[i2])
                    if nb1 < nb2:
                        ia = i1
                        i1 = i2
                        i2 = ia
                    # we merge 2 -> 1
                    l2 = list(sets[i2])
                    for x in l2:
                        setIdx[x] = i1
                        sets[i1].add(x)
                    del sets[i2]
                    if pmNb in sets[i1]:
                        pmSetIdx = i1
                        pmSetSize = len(sets[i1])
            if pmSetSize >= 990000:
                return r
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
