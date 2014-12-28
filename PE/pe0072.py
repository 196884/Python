def solve():
    # this is directly the sum of the phi(m), for m from 2 to 1000000
    # we first sieve...
    b = 1000001
    isPrime = [True for i in range(0, b)]
    hFactor = [None for i in range(0, b)]
    # hFactor[n] will contain (p, p^k), where:
    # * p is the largest prime factor of n
    # * p^k is the highest power of p dividing n

    for n in range(2, b):
        if isPrime[n]:
            pk = n
            while pk < b:
                mpk = pk
                while mpk < b:
                    isPrime[mpk] = False
                    hFactor[mpk] = (n, pk)
                    mpk += pk
                pk *= n
    phi = [1 for i in range(0, b)]
    r = 0
    for i in range(2, b):
        (p, pk) = hFactor[i]
        aux = (pk / p) * (p-1) * phi[i / pk]
        phi[i] = aux
        r += aux
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
