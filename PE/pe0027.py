# We're looking for a and b with
# Abs(a) < 1000, Abs(b) < 1000,
# and n^2+an+b prime for a max number of consecutive n's,
# starting at 0
#
# b has to be prime and odd
# a has to be odd
import array as array

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
    primes = primeSieve(1000000)
    ra = 0
    rb = 0
    n = 0
    primeSet = set(primes)
    for b in primes:
        if b >= 1000:
            return ra * rb
        for a in range(-1000, 1001):
            if a % 2 == 1:
                c = b
                d = 0
                while c in primeSet:
                    c += 2 * d + a + 1
                    d += 1
                if d > n:
                    ra = a
                    rb = b
                    n = d

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
