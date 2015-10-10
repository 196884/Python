import random as rand

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
    # We write n-1 = 2^r.d
    d = n - 1
    r = 0
    while d % 2 == 0:
        r += 1
        d /= 2
    for a in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]:
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

def rowEnd(n):
    return n * (n+1) / 2

def rowStart(n):
    return 1 + rowEnd(n-1)

# Row i has i elements, index from j=0 to j=i-1:
def rowElement(i, j):
    if j < 0 or j >= i:
        return 0
    return rowEnd(i-1) + 1 + j

cache = dict()

def isElementPrime(i, j):
    element = rowElement(i, j)
    if element == 0:
        return False
    cached = cache.get(element, None)
    if cached != None:
        return cached
    #result = isPrime(element, primes)
    result = millerRabin(element)
    cache[element] = result
    return result

def checkAt(i, j):
    if isElementPrime(i, j):
        n1 = 0
        for (di1, dj1) in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            i1 = i + di1
            j1 = j + dj1
            if isElementPrime(i1, j1):
                n1 += 1
                if n1 == 2:
                    return True
                for (di2, dj2) in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    if di1 + di2 != 0 or dj1 + dj2 != 0:
                        i2 = i1 + di2
                        j2 = j1 + dj2
                        if isElementPrime(i2, j2):
                            return True
    return False

def doRow(n):
    r = 0
    for c in range(0, n):
        if checkAt(n, c):
            r += rowElement(n, c)
        if c % 1000 == 0:
            print (c, n)
    return r
      
def solve():
    # Brute force...
    row1 = 5678027
    row2 = 7208785
    r  = 0
    r += doRow(row1)
    r += doRow(row2)
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
