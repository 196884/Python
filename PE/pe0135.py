def solve():
    # Yet another pretty naive one...
    B = 10 ** 6
    pInfo = [ (1, 1) for n in range(0, B+1) ]
    factors = [[1], [1]]
    r = 0
    for n in range(2, B+1):
        c = 0
        (p, pk) = pInfo[n]
        if 1 == p:
            # n is prime
            p = n
            pk = p
            while pk <= B:
                pkm = pk
                while pkm <= B:
                    pInfo[pkm] = (p, pk)
                    pkm += pk
                pk *= p
            factors.append([1, p])
        else:
            pl = 1
            aux = factors[n / pk]
            fl = []
            while pl <= pk:
                for fa in aux:
                    f = pl * fa
                    fnf = n / f + f
                    if fnf % 4 == 0:
                        b = fnf / 4
                        if b < f:
                            c += 1
                    fl.append(f)
                pl *= p
            factors.append(fl)
            if 10 == c:
                r += 1
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
