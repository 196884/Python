def solve():
    B = 10 ** 7
    pInfo = [(1, 1) for n in range(0, B+1)]
    cache = dict()
    for n in range(2, B+1):
        (p, pk) = pInfo[n]
        if 1 == p:
            p = n
            pk = p
            while pk <= B:
                pkm = pk
                while pkm <= B:
                    pInfo[pkm] = (p, pk)
                    pkm += pk
                pk *= p
        else:
            qk = n / pk
            qI = pInfo[qk]
            if qk > 1 and qI[1] == qk:
                q = qI[0]
                cache[(q, p)] = n
    return sum(cache.values())

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
