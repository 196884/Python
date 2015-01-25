def solve():
    # Naive, but good enough
    B = 20000000
    pInfo = [(1, 1, 0) for n in range(0, B+1)]
    l = [0 for n in range(0, B+1)]
    for n in range(2, B+1):
        if n % 1000 == 0:
            print n
        (p, pk, spk) = pInfo[n]
        if 1 == p:
            # n is prime
            p = n
            pk = p
            spk = p
            while pk <= B:
                mpk = pk
                while mpk <= B:
                    pInfo[mpk] = (p, pk, spk)
                    mpk += pk
                pk *= p
                spk += p
            l[p] = p
        else:
            l[n] = spk + l[n / pk]
    s1 = sum(l)
    s2 = sum(l[:15000001])
    s3 = sum(l[:5000001])
    return s1 - s2 - s3

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
