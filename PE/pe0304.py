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

def getPrimes(B):
    primes = []
    isPrime = [True for n in range(0, B+1)]
    for n in range(2, B+1):
        if isPrime[n]:
            p = n
            primes.append(p)
            pk = 2 * p
            while pk <= B:
                isPrime[pk] = False
                pk += p
    return primes

def isPrime(n, primes):
    for p in primes:
        if n % p == 0:
            return n == p
    return True

def fib(n, x):
    m = [[0, 1], [1, 1]]
    m = powModMat2(m, n, x)
    return m[1][0]

def solve():
    # Really slow in Python. Could speed up the sieving, but enough for now
    B = 10 ** 7 + 10 ** 4
    primes = getPrimes(B)
    n = 10 ** 14
    m = 1234567891011
    r = 0
    k = 0
    while True:
        n += 1
        if isPrime(n, primes):
            r += fib(n, m)
            k += 1
            print k
            if k == 10 ** 5:
                return r % m

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
