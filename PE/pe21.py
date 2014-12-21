# In order to get the total factorization of all consecutive integers, we do as follows:
# * We sieve (up to a point)
# * at the pass when we divide n by p^k, we store p^k (and p and k) at index
#   n in an array ('largest factor')

def genFactorsInfo(b):
    """
    fi[n] = (p, k, p^k, [1, p,..., p^k]) where
    * p is the largest prime factor of n
    * k is the largest integer such that p^k divides n
    """
    fi = [(1, 1, 1, []) for i in range(0, b+1)]
    factors = [([1], 0), ([1], 0)]
    result = 0
    for n in range(2, b+1):
        a = fi[n][0]
        if a == 1:
            # Case where n is prime:
            k = 0
            pkl = [1]
            pk = n
            while pk <= b:
                # We actually handle pk here
                k += 1
                pkl.append(pk)
                # We tag all of the multiples of pk
                pkm = pk
                pklc = list(pkl) # Forcing a deep copy
                while pkm <= b:
                    fi[pkm] = (n, k, pk, pklc)
                    pkm += pk
                pk *= n
        pk = fi[n][2]
        pl = fi[n][3]
        ql = factors[n / fi[n][2]][0]
        fs = [ x * y for x in pl for y in ql ]
        d  = sum(fs) - n
        if d < n and n == factors[d][1]:
            result += n + d
        factors.append(([ x * y for x in pl for y in ql ], d))
    return result

def solve():
    return genFactorsInfo(10000)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

