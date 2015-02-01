def solve():
    # Very naive... but works
    B = 10 ** 7
    pInfo = [ (1, 1) for n in range(0, B+1) ]
    r = 0
    for n in range(2, B+1):
        if n % 1000 == 0:
            print n
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
            r += 1
        elif n == pk:
            r += 1
        else:
            f = n - pk
            found = False
            while not found:
                if f * (f + 1) % n == 0:
                    r += f + 1
                    found = True
                elif f * (f - 1) % n == 0:
                    r += f
                    found = True
                f -= pk
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
