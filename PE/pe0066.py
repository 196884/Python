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

def sqrtCF(n):
    #print "Doing %d" % n
    q0 = iSqrt(n)
    if q0 * q0 == n:
        return 0
    cache = dict()
    # The current element is of the form:
    # (sqrt(n)-a) / b
    # where b divides n-a^2 (proof by induction)
    r = [ q0 ]
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
        r.append(qNew)
        if cached != None:
            return (r, i - cached)
        else:
            cache[(aNew, bNew)] = i
        a = aNew
        b = bNew

def evalConvergent(l, k):
    k -= 1
    if k == 0:
        return (l[0], 1)
    p = len(l) - 1
    i = k % p
    if i == 0:
        i = p
    n = l[i]
    d = 1
    k -= 1
    while k > 0:
        i = k % p
        if i == 0:
            i = p
        x = l[i]
        aux = n
        n = n * x + d
        d = aux
        k -= 1
    aux = n
    n = n * l[0] + d
    d = aux
    return (n, d)

def solve():
    r = 0
    nMax = 0
    for D in range(1, 1000):
        Dsqrt = iSqrt(D)
        if Dsqrt ** 2 != D:
            (cf, p) = sqrtCF(D)
            k = len(cf) - 1
            if k % 2 == 1:
                k *= 2
            (n, d) = evalConvergent(cf, k)
            if n > nMax:
                nMax = n
                r = D
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
