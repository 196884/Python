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

def sqrtCFPeriod(n):
    #print "Doing %d" % n
    q0 = iSqrt(n)
    if q0 * q0 == n:
        return 0
    cache = dict()
    # The current element is of the form:
    # (sqrt(n)-a) / b
    # where b divides n-a^2 (proof by induction)
    a = q0
    b = 1
    cache[(a, b)] = 0
    i = 0
    while True:
        i += 1
        bNew = (n - a * a) / b
        qNew = (q0 + a) / bNew
        aNew = qNew * bNew - a
        cached = cache.get((aNew, bNew), None)
        if cached != None:
            return i - cached
        else:
            cache[(aNew, bNew)] = i
        a = aNew
        b = bNew

def solve():
    r = 0
    for n in range(2, 10000):
        p = sqrtCFPeriod(n)
        if p % 2 == 1:
            r += 1
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
