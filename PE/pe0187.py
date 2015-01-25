def solve():
    H = 10 ** 8
    B = H / 2
    isPrime = [True for i in range(0, B)]
    primes = []
    # We sieve for the primes
    for n in range(2, B):
        if isPrime[n]:
            p = n
            primes.append(p)
            pk = 2 * p
            while pk < B:
                isPrime[pk] = False
                pk += p
    # Now we count the products...
    r = 0
    j = len(primes) - 1
    for i, p in enumerate(primes):
        while p * primes[j] > H:
            j -= 1
        if primes[j] < p:
            return r
        r += j - i + 1
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
