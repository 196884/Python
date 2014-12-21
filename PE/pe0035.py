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

def isPrime(n, primes):
    if n == 1:
        return False
    for p in primes:
        if n % p == 0:
            return n == p
    return True

def solveLenK(k, primes):
    """
    only looks for solutions of exactly k digits:
    """
    b = 4 ** k
    f = 10 ** (k-1)
    db = [1, 3, 7, 9]
    result = 0
    for i in range(0, b):
        n = 0
        ii = i
        for j in range(0, k):
            n = 10 * n + db[ii % 4]
            ii /= 4
        j = 0
        while j < k and isPrime(n, primes):
            d = n % 10
            n = n / 10 + d * f
            j += 1
        if j == k:
            result += 1
    return result

def solve():
    # Apart from 2 and 5, the numbers can only contain the digits:
    # 1, 3, 7, 9
    primes = primeSieve(1000)
    result = 2 # for 2 and 5
    for k in range(1, 8):
        result += solveLenK(k, primes)
    return result

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
