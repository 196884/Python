# The goal is to return the largest prime factor of
# 600851475143

import array

def powMod(a, b, m):
    a2k    = a # a^(2^k)
    result = 1
    while b > 0:
        if b % 2 == 1:
            result = (result * a2k) % m
        a2k = (a2k * a2k) % m
        b /= 2
    return result

def multModMat2(l1, l2, m):
    r = [[0, 0], [0, 0]]
    r[0][0] = (l1[0][0] * l2[0][0] + l1[0][1] * l2[1][0]) % m
    r[0][1] = (l1[0][0] * l2[0][1] + l1[0][1] * l2[1][1]) % m
    r[1][0] = (l1[1][0] * l2[0][0] + l1[1][1] * l2[1][0]) % m
    r[1][1] = (l1[1][0] * l2[0][1] + l1[1][1] * l2[1][1]) % m
    return r

def powModMat2(l, n, m):
    # l is supposed to be a 2x2 matrix, computes l^n mod m
    l2k = l
    result = [[1, 0], [0, 1]]
    while n > 0:
        if n % 2 == 1:
            result = multModMat2(result, l2k, m)
        l2k = multModMat2(l2k, l2k, m)
        n /= 2
    return result

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

def solve():
    p = 10 ** 9 + 7
    b = iSqrt(p)
    primes = primeSieve(b)
    for n in primes:
        if p % n == 0:
            return 0

    N = 11 ** 14
    l1 = [[-1, 1], [1, 0]]
    lN = powModMat2(l1, N, p-1)
    l0 = lN[0][0]
    l1 = lN[0][1]
    betaN = (l0 + 3 * l1) % (p-1)
    gammaN = (l0 + l1) % (p-1)
    result = 0
    k = (-2 * gammaN - 1) % (p-1)
    result += powMod(3, k, p)
    k = (2 * betaN - 2) % (p-1)
    result += powMod(2, k, p)
    k = (betaN-2) % (p-1)
    aux = powMod(2, k, p)
    k = (-gammaN-1) % (p-1)
    aux = (aux * powMod(3, k, p)) % p
    result += aux
    k = (2*betaN+2) % (p-1)
    result += powMod(2, k, p)
    k = (1-2*gammaN) % (p-1)
    result -= powMod(3, k, p)
    aux = powMod(2, betaN, p)
    k = (-gammaN) % (p-1)
    aux = (aux * powMod(3, k, p)) % p
    result += aux
    result = result % p
    return result

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
