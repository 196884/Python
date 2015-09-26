import array

def primeSieve(n):
    """ 
    Returns all prime numbers <= n via Eratosthene's sieve
    """
    result = []
    sieve = array.array('i', (True for i in range(0, n+1)))
    for k in range(2, n+1):
        if sieve[k]:
            result.append(k)
            i = k * k
            while i <= n:
                sieve[i] = False
                i += k
    return result

def sortFn((a, b, c)):
    return c

def solve():
    primes = primeSieve(9 * 10**6)
    print "Generated primes..."
    m = 500500507
    r = 1
    k = 1 # index of the next prime to consider in 'primes'
    product = 2
    auxIdx = 1 # index of the next prime to consider for inclusion in aux
    aux = [(2, 1, 4)] # (p, b, p^(2^b)), sorted by p^(2^b) increasing
    fMin = aux[0][2]
    for r in range(500499):
        p = primes[k]
        if p < fMin:
            product = (product * p) % m
            k += 1
        else:
            product = (product * fMin) % m
            (p, b, f) = aux[0]
            aux[0] = (p, b+1, p**(2**(b+1)))
            if b == 1:
                q = primes[auxIdx]
                auxIdx += 1
                aux.append((q, 1, q * q))
            aux.sort(key = sortFn)
            fMin = aux[0][2]
    return product

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
