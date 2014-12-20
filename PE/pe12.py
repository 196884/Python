# In order to get the total factorization (actually, only the total number
# of factors is needed) of all consecutive integers, we do as follows:
# * We sieve (up to a point)
# * at the pass when we divide n by p^k, we store p^k (and p and k) at index
#   n in an array ('largest factor')

def genFactorsInfo(n):
    """
    Not really used here, but does only the factorization
    """
    result = [(1, 1, 1) for i in range(0, n+1)]
    nbMults = [ 1, 1 ]
    p = 2
    while p <= n:
        (a, b, c) = result[p]
        if a == 1:
            # Case where p is prime:
            k = 1
            pk = p
            while pk <= n:
                pkm = pk
                while pkm <= n:
                    result[pkm] = (p, k+1, pk)
                    pkm += pk
                pk *= p
                k += 1
        (_, b, c) = result[p] # the above has updated it
        thisMult = b * nbMults[p / c]
        nbMults.append(thisMult)
        p += 1
    return (result, nbMults)

def solve():
    n = 100000 # Wild guess
    result = [(1, 1, 1) for i in range(0, n+1)]
    nbMults = [ 1, 1 ]
    bound = 500
    # Special adjustment: since at the end we test
    # k * (k + 1) / 2
    # and only one of k and k+1 is even, we store in nbMults
    # and results the data corresponding to the index, *divided
    # by 2 if even*
    k = 1
    pk = 2
    while pk <= n:
        pkm = pk
        while pkm <= n:
            result[pkm] = (2, k, pk) # k here because of the special case
            pkm += pk
        pk *= 2
        k += 1
    nbMults.append(1)
    p = 3
    while p <= n:
        (a, b, c) = result[p]
        if a == 1:
            # Case where p is prime:
            k = 1
            pk = p
            while pk <= n:
                pkm = pk
                while pkm <= n:
                    result[pkm] = (p, k+1, pk)
                    pkm += pk
                pk *= p
                k += 1
        (_, b, c) = result[p] # the above has updated it
        thisMult = b * nbMults[p / c]
        prevMult = nbMults[-1]
        tMults = thisMult * nbMults[-1]
        if tMults > bound:
            return p * (p-1) / 2
        nbMults.append(thisMult)
        p += 1
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

