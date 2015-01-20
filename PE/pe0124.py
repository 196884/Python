def solve():
    b = 100000
    pInfo = [(1, 1) for i in range(0, b+1)]
    rad = [1]
    for n in range(2, b+1):
        (p, pk) = pInfo[n]
        if 1 == p:
            # n is prime
            p = n
            pk = p
            while pk <= b:
                pkm = pk
                while pkm <= b:
                    pInfo[pkm] = (p, pk)
                    pkm += pk
                pk *= p
        (p, pk) = pInfo[n]
        rad.append(p * rad[n / pk - 1])
    l = [(rad[i], i+1) for i in range(0, b)]
    l.sort()
    return l[9999][1]

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
