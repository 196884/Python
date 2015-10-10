import random as rand
import array

def gcd(a, b):
    if a == b:
        return a
    if a < b:
        return gcd(b, a)
    if b == 0:
        return a
    return gcd(b, a%b)

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

def powMod(a, b, m):
    a2k    = a # a^(2^k)
    result = 1
    while b > 0:
        if b % 2 == 1:
            result = (result * a2k) % m
        a2k = (a2k * a2k) % m
        b /= 2
    return result

def millerRabin(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    basis = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    for p in basis:
        if n == p:
            return True
    # We write n-1 = 2^r.d
    d = n - 1
    r = 0
    while d % 2 == 0:
        r += 1
        d /= 2
    for a in basis:
        x = powMod(a, d, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < r:
                x = (x * x) % n
                if x == 1:
                    return False
                if x == n-1:
                    j = r + 10
                j += 1
            if j < r + 10:
                return False
    return True

def tFn(n):
    return 2 * n * n - 1

def jacobiSymbol(a, n):
    r = 1
    while True:
        if n > 1:
            a = a % n
        if a == 0:
            return 0
        p2 = 0
        while a % 2 == 0:
            p2 += 1
            a /= 2
        if p2 % 2 == 1:
            n8 = n % 8
            if n8 == 3 or n8 == 5:
                r *= -1
        if n == 1:
            return r
        if gcd(a, n) > 1:
            return 0
        if a % 4 == 3 and n % 4 == 3:
            r *= -1
        aux = a
        a = n
        n = aux

def solve():
    # Slow, bruteforce... could/should have used p+1
    r = 0
    for n in range(2, 50000000):
        t = tFn(n)
        if millerRabin(t):
            r += 1
        if n % 10000 == 0:
            print n
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
