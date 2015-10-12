def sFn((a, b, c, d, e, f)):
    return (b, c, d, e, f, a ^ (b & c))

def fromBinary((a, b, c, d, e, f)):
    return 32 * a + 16 * b + 8 * c + 4 * d + 2 * e + f

def solve():
    trans = dict()
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    for e in range(2):
                        for f in range(2):
                            cfg = (a, b, c, d, e, f)
                            sCfg = sFn(cfg)
                            n = fromBinary(cfg)
                            sn = fromBinary(sCfg)
                            if n != sn:
                                s = trans.get(n, set())
                                s.add(sn)
                                trans[n] = s
                                t = trans.get(sn, set())
                                t.add(n)
                                trans[sn] = t
    l = []
    for n in range(2**6):
        t = trans.get(n, None)
        if t == None:
            l.append([False, []])
        else:
            l.append([True, list(t)])
    for i, (t, u) in enumerate(l):
        print (i, u)
    # Ah, now that we have the graph: it is made of 5 disconnected cycles
    # (each cycle has doubly directed edges), of lengths (2, 3, 6, 6, 46),
    # and it's easy to see that the number of possible functions on a cycle of
    # p elements is F(p-1) + F(p+1) (F the Fibonacci function), so:
    c = [2, 3, 6, 6, 46]
    F = [0, 1]
    for k in range(2, 50):
        F.append(F[-1] + F[-2])
    r = 1
    for p in c:
        r *= F[p-1] + F[p+1]
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
