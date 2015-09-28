import array

def iSqrt(n):
    """
    Integral square root (by Newton iterations)
    """
    x    = 1
    xOld = 1
    while True:
        aux = ( x + ( n / x ) ) / 2
        if aux == x:
            return x
        if aux == xOld:
            return min(x, xOld)
        xOld = x
        x = aux

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

def naiveFactorization(n):
    sqrt = iSqrt(n)
    primes = primeSieve(sqrt)
    result = []
    r = n
    for p in primes:
        q = 0
        while r % p == 0:
            q += 1
            r  = r / p
        if q > 0:
            result.append((p, q))
        if 1 == r:
            return result
    result.append((r, 1))
    return result

def naiveM(n):
    c = [1 for i in range(n)]
    r = 0
    pos = 0
    pl = [pos]
    done = False
    while not done:
        k = c[pos]
        done = k == n
        r += 1
        c[pos] = 0
        for i in range(k):
            pos = (pos + 1) % n
            c[pos] += 1
        pl.append(pos)
    return (r, pl)

def naiveMTrace(n):
    c = [1 for i in range(n)]
    r = 0
    pos = 0
    pl = [pos]
    done = False
    while not done:
        k = c[pos]
        done = k == n
        r += 1
        c[pos] = 0
        for i in range(k):
            pos = (pos + 1) % n
            c[pos] += 1
        pl.append(pos)
        print r
        print c
    return (r, pl)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        (g, y, x) = egcd(b % a, a)
        return (g, x - (b / a) * y, y)

def modInv(a, p):
    (g, x, y) = egcd(a, p)
    return x % p

def modPow(a, k, p):
    bits = []
    while k > 0:
        bits.append(k % 2)
        k /= 2
    r = 1
    for bit in reversed(bits):
        r = r * r % p
        if bit == 1:
            r = r * a % p
    return r


def solve():
    # if n = 2^k + 1, then the size of the cycle is:
    # n=5
    # 3 * 3 + 5 + 1
    # n=9
    # 7 * 5 + 9 + (2+2**2) + 3
    # n=17
    # 15 * 9 + 17 + (2**2+...+2**4) + 3(2+2**2) + 3**2
    # n=33
    # 31 * 17 + 33 + (2**3+...+2**6) + 3(2**2+...+2**4) + 3**2(2+2**2) + 3**3
    # n=65:
    # 63 * 33 + 65 + (2**4+2**5+2**6+2**7+2**8) + 3(2**3+2**4+2**5+2**6) + 3**2(2**2+2**3+2**4) + 3**3(2+2**2) + 3**4
    # n = 129:
    # 127 * 65 + 129 + (2**5+...+2**10) + 3(2**4+...+2**8) + 3**2(2**3+...+2**6) + 3**3(2**2+...+2**4) + 3**4(2 + 2**2) + 3**5
    #
    # this can be proven by induction, by checking how long it takes to go to:
    # * 1(02)^(2^(k-1))
    # * 1(0004)^(2^(k-2))
    # * 1(00000008)^(2^(k-3))
    # * ...
    # * 1(0)^(2^k-1)(2^k)
    # and it's then clear that it takes 2^k+1 steps from that above configuration to go back to the 1* one
    #
    # From this, one shows that:
    # M(2^k+1) = 2**(2*k)+2**(k+1)-3**k
    # Now the result is straightforward
    n = 10**18
    m = 7**9
    a = (modPow(4, n+1, m) - 1) * modInv(3, m) % m
    b = (modPow(2, n+1, m) - 1) * 2 % m
    c = (modPow(3, n+1, m) - 1) * modInv(2, m) % m
    r = a + b - c
    r = r % m
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
