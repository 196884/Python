# The goal is to return the largest prime factor of
# 600851475143

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

def solve():
    primes = primeSieve(100)
    r = 1
    for p in primes:
        if p * r < 1000000:
            r *= p
        else:
            return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
