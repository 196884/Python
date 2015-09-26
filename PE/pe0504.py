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

def isSquare(n):
    r = iSqrt(n)
    return r * r == n

def gcd(a, b):
    if a == b:
        return a
    if a < b:
        return gcd(b, a)
    if b == 0:
        return a
    return gcd(b, a%b)

def triangleCount(a, b, c):
    # number of points in the triangle [(0,-a), (0,b), (c, 0)]
    # does *not* include the a+b-1 points on the x axis
    r = c - 1 + ( (a-1) * (c-1) - gcd(a, c) + 1 ) / 2 + ( (b-1) * (c-1) - gcd(b, c) + 1 ) / 2
    return r

def solve():
    N = 100 
    r = 0
    for a in range(1, N+1):
        for b in range(1, a+1):
            nab = 0
            print (a, b)
            byC = []
            for c in range(1, N+1):
                tc = triangleCount(a, b, c)
                byC.append(tc)
            for i in range(0, N):
                for j in range(0, i+1):
                    total = byC[i] + byC[j] + a + b - 1
                    if isSquare( total ):
                        if i == j:
                            nab += 1
                        else:
                            nab += 2
            if a == b:
                r += nab
            else:
                r += 2 * nab
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
