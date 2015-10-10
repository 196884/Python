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

def digits(n):
    r = []
    c = False
    p1 = 1
    p2 = 1
    while n > 0:
        d = n % 10
        r.append(d)
        n /= 10
        c = c or ( d == 2 and p1 == 0 and p2 == 0 )
        p2 = p1
        p1 = d
    return (c, r)

def isPrime(n, primes):
    if n == 0:
        return False
    for p in primes:
        if p * p > n:
            return True
        if n % p == 0:
            return False
    return None

def check(n, ds, primes):
    for k, d in enumerate(ds):
        for f in range(10):
            np = n + 10**k * (f-d)
            if isPrime(np, primes):
                return False
    return True

def solve():
    # Brute force...
    primes = primeSieve(10**6)
    print "Primes generated..."
    B = 1000000000000
    primesBasis = primes[:5000]
    candidates = []
    i = 0
    q3 = primes[i] ** 3
    while q3 < B:
        j = 0
        p2 = primes[j] ** 2
        while q3 * p2 < B:
            if i != j:
                candidates.append(p2 * q3)
            j += 1
            p2 = primes[j] ** 2
        i += 1
        q3 = primes[i] ** 3
    candidates.sort()
    print "Candidates generated..."
    k = 0
    for n in candidates:
        (c, ds) = digits(n)
        if c:
            if check(n, ds, primes):
                k += 1
                if k == 200:
                    return n
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
