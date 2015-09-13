import array

def gcd(a, b):
    if b > a:
        return gcd(b, a)
    if b == 0:
        return a
    return gcd(b, a%b)

def iSqrt(n):
    if n == 0:
        return 0
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

def arePrime(l, primes):
    for p in primes:
        for n in l:
            if (p < n) and (n % p == 0):
                return False
    return True

def isPrime(n, primes):
    for p in primes:
        if p >= n:
            return True
        if n % p == 0:
            return False
    return True

def genGaussPrimes(n):
    m = iSqrt(n)
    d = array.array('i', (0 for i in range(0, n+1)))
    print "starting genGaussPrimes loop..."
    for a in range(1, m+1):
        print a
        # We want a^2 + b^2 <= n, so
        a2 = a * a
        bMax = iSqrt(n-a*a)
        for b in range(1, bMax+1):
            if gcd(a, b) == 1:
                norm = a2 + b * b
                d[a2 + b * b] += 2 * a
    return d

def sumDivisors(n):
    rl    = [0, 1]
    qa    = array.array('i', (1 for i in range(0, n+1)))
    qpowa = array.array('i', (1 for i in range(0, n+1)))
    print "starting sumDivisors loop..."
    for k in range(2, n+1):
        if qa[k] == 1:
            # Case where k is prime:
            p = k
            rl.append(p+1)
            ppow = p
            while ppow <= n:
                ppowMul = ppow
                while ppowMul <= n:
                    qa[ ppowMul ] = p
                    qpowa[ ppowMul ] = ppow
                    ppowMul += ppow
                ppow *= p
        else:
            # k is not prime
            aux = rl[ k / qpowa[k] ] * (qpowa[k] * qa[k] - 1) / (qa[k] - 1)
            rl.append( aux )
        if k < 1000:
            print k
        else:
            if k % 1000 == 0:
                print k
    return rl

def sumGaussDivisors(n):
    sd = sumDivisors(n)
    print "sd generated"
    d  = genGaussPrimes(n)
    print "d generated"
    r  = 0
    for k in range(1, n+1):
        r += sd[k]
        a  = d[k]
        if a > 0:
            bMax = n / k
            for b in range(1, bMax+1):
                r += a * sd[b]
    return r

def solve():
    # Not the most efficient surely, but does the trick
    n = 10**8
    return sumGaussDivisors(n)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
