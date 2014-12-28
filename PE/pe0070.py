def permKey(n):
    l = list(str(n))
    l.sort()
    return(int("".join(l)))

def solve():
    # We check smooth numbers with no square factors in priority, as
    # these would minimize n / phi(n)

    # A faster method would be to try an generate them from small primes directly,
    # going to the upper prime whenever the product would go over 10**7 (this way,
    # the first n enumerated such that phi(n) is a permutation of n would be the solution,
    # as we would generate all the possible values of the ratio n/phi(n) in decreasing order)

    # this is directly the sum of the phi(m), for m from 2 to 1000000
    # we first sieve...
    b = 10000001
    isPrime = [True for i in range(0, b)]
    phiDict = dict()
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

    phi = [(1, True) for i in range(0, b)]
    l = []
    bn = 1
    bp = 0
    for i in range(2, b):
        (p, pk) = hFactor[i]
        if p == pk:
            (c, d) = phi[i / p]
            if d:
                aux = c * (p-1)
                phi[i] = (aux, True)
                if permKey(i) == permKey(aux):
                    if i * bp < aux * bn:
                        bp = aux
                        bn = i
    return bn

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
