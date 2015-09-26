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

def dr(n):
    while n >= 10:
        r = 0
        while n > 0:
            r += n % 10
            n /= 10
        n = r
    return n

def solve():
    N = 10**6
    mdrs = [0, 0]
    for n in range(2, N):
        maxSoFar = dr(n)
        maxF = iSqrt(n)
        for f1 in range(2, maxF + 1):
            if n % f1 == 0:
                f2 = n / f1
                maxSoFar = max(maxSoFar, mdrs[f1] + mdrs[f2])
        mdrs.append(maxSoFar)
    return sum(mdrs)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
