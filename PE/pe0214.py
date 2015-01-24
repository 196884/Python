def solve():
    # Naive, slow-ish, but good enough
    B = 40000000
    # pInfo[n] = (p, p^k) where:
    pInfo = [(1, 1) for i in range(0, B+1)]
    phi = [1 for i in range(0, B+1)]
    l = [1 for i in range(0, B+1)]
    # * p is the largest prime factor of n
    # * p^k is the highest power of p dividing n
    r = 0
    for n in range(2, B+1):
        (p, pk) = pInfo[n]
        isPrime = False
        if 1 == p:
            isPrime = True
            p = n
            pk = p
            phi[n] = p - 1
            while pk <= B:
                mpk = pk
                while mpk <= B:
                    pInfo[mpk] = (p, pk)
                    mpk += pk
                pk *= p
        else:
            phi[n] = (pk / p) * (p - 1) * phi[n / pk]
        l[n] = 1 + l[phi[n]]
        if isPrime and 25 == l[n]:
            r += n
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
