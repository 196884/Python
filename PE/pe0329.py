B = 500
K = 15

def gcd(a, b):
    if a == b:
        return a
    if a < b:
        return gcd(b, a)
    if b == 0:
        return a
    return gcd(b, a%b)

pattern = [True, True, True, True, False, False, True, True, True, False, True, True, False, True, False]

cache = dict()

def getProbaNum(n, k, isPrime):
    if K == k:
        return 1
    cached = cache.get((n, k), None)
    if cached != None:
        return cached
    if isPrime[n] == pattern[k]:
        num = 2
    else:
        num = 1
    if n == 1:
        num *= 2 * getProbaNum(2, k+1, isPrime)
    elif n == B:
        num *= 2 * getProbaNum(B-1, k+1, isPrime)
    else:
        num *= ( getProbaNum(n-1, k+1, isPrime) + getProbaNum(n+1, k+1, isPrime) )
    cache[(n, k)] = num
    return num

def solve():
    # Naive, but good enough
    isPrime = [True for x in range(0, B+1)]
    isPrime[1] = False
    for n in range(2, B+1):
        if isPrime[n]:
            # n is prime
            p = n
            pk = p * 2
            while pk <= B:
                isPrime[pk] = False
                pk += p

    # The denominator is always going to be 2^14 * 3^15
    num = 0
    for n in range(1, B+1):
        num += getProbaNum(n, 0, isPrime)
    denom = B * 2 ** K * 3 ** K
    g = gcd(num, denom)
    print "%d/%d" % (num / g, denom / g)
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
