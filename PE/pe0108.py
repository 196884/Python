def solve():
    # If we let:
    #     a = g.x
    #     b = g.y
    # where g is the gcd of a and b, then we must have:
    #     n = g.x.y / (x + y)
    # in particular, we must have x and y two coprime divisors of n.
    # 
    # Conversely, given two such x and y, one can always find a multiplier
    # to get n.
    # 
    # Now, if we have n=p1^n1.p2^n2...., then computing the number of couples
    # (x, y) as above is quite straightforward:
    #     F(n) = 1 + n1 + (2.n1 + 1) (F(n/p1^n1) - 1)
    # 
    # We implement this. Note that we expect to find large number of solutions
    # for smooth n, of course

    # first, we sieve to get the decompositions...
    b = 1000000
    pInfo = [(1, 1, 1) for i in range(0, b+1)]
    F     = [1 for i in range(0, b+1)]
    for n in range(2, b+1):
        (fMax, k, pk) = pInfo[n]
        if fMax == 1:
            # case where n is prime
            nk = n
            k = 1
            while nk <= b:
                nkm = nk
                while nkm <= b:
                    pInfo[nkm] = (n, k, nk)
                    nkm += nk
                nk *= n
                k += 1
        (fMax, k, pk) = pInfo[n] # Now updated...
        F[n] = 1 + k + ( 2 * k + 1 ) * (F[n / pk] - 1)
        if F[n] >= 1000:
            return n
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
