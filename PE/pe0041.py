# Looking for the largest n-pandigital prime, for 1<=n<=9
# Since 3 divides 1+2+3+4+5+6+7+8+9, we must have n<=8
# 
# The last digit cannot be 2, 4, 5, 6 or 8, which leaves
# 3 possibilities (1, 3, 7)
#
# Overall, this gives 3x7! = 15120 admissible permutations
# of [1, 8], so the plan is to test the primality of each of them.
# 
# To go faster, we can start with the highest value (87654321)
# and generate the permutations in descending lexicographic order
# from there.

import array

def prevPerm(l):
    n = len(l)
    i = n - 1
    while i > 0 and l[i-1] <= l[i]:
        i -= 1
    if i <= 0:
        return list(reversed(l))
    j = n - 1
    while l[j] >= l[i-1]:
        j -= 1
    tmp = l[i-1]
    l[i-1] = l[j]
    l[j] = tmp
    j = n - 1
    while i < j:
        tmp = l[i]
        l[i] = l[j]
        l[j] = tmp
        i += 1
        j -= 1
    return l

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
        if p * p > n:
            return True
    return True

def arrayToInt(l):
    r = 0
    for x in l:
        r = 10 * r + x
    return r

def solve():
    # Tested the 8 digit case... no luck
    nMax   = 7654321
    pMax   = iSqrt(nMax)
    primes = primeSieve(pMax)
    l      = [7, 6, 5, 4, 3, 2, 1]
    while True:
        if l == [1, 2, 3, 4, 5, 6, 7]:
            return 0
        if l[6] == 1 or l[6] == 3 or l[6] == 7:
            n = arrayToInt(l)
            if isPrime(n, primes):
                return n
        l = prevPerm(l)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
