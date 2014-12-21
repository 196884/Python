# We start from the code of pe21.py

def genAbundant(b):
    """
    fi[n] = (p, k, p^k, [1, p,..., p^k]) where
    * p is the largest prime factor of n
    * k is the largest integer such that p^k divides n
    """
    fi = [(1, 1, 1, []) for i in range(0, b+1)]
    factors = [([1], 0), ([1], 0)]
    result = []
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
        if d > n:
            result.append(n)
        factors.append(([ x * y for x in pl for y in ql ], d))
    return result

def solve():
    # From the question, we know that numbers above 28123
    # are sum of two abundant numbers
    b = 23123
    abundantList = genAbundant(b)
    n = len(abundantList)
    okSet = set()
    for i in range(0, n):
        j = i
        ai = abundantList[i]
        aj = abundantList[j]
        while j < n and ai + aj <= b:
            okSet.add(ai+aj)
            j += 1
            if j < n:
                aj = abundantList[j]
    result = 0
    for x in range(1, b+1):
        if x not in okSet:
            result += x
    return result

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

