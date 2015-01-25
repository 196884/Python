def auxRec(d, k, ppow, B):
    """
    Parameters:
    d is the factor we have
    k is the number of distinct primes already used
    ppow is as generated in 'solve' below (ppow[i] is the list of successive powers
    of the i-th prime that are <= B)
    B is the bound
    """
    if k >= len(ppow):
        return 1
    r = 0
    ppk = ppow[k]
    for pk in ppk:
        pkd = pk * d
        if pkd > B:
            return r
        r += auxRec(pkd, k+1, ppow, B)
    return r

def solve():
    # Another naive one...
    B = 100
    primes = []
    isPrime = [ True for n in range(0, B+1) ]
    for n in range(2, B+1):
        if isPrime[n]:
            p = n
            primes.append(p)
            pk = 2 * p
            while pk <= B:
                isPrime[pk] = False
                pk += p
    ppow = []
    B = 10 ** 9
    for p in primes:
        l = [1]
        pp = p
        while pp <= B:
            l.append(pp)
            pp *= p
        ppow.append(l)
    r = auxRec(1, 0, ppow, B)
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
