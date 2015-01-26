def genPal(p10, p, odd):
    s = 0
    q = p
    while q > 0:
        s = 10 * s + q % 10
        q /= 10
    if odd:
        p /= 10
    p *= p10
    return p + s

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

def check(p):
    r = 0
    k = 1
    k3 = k * k * k
    while k3 < p:
        sq = iSqrt(p - k3)
        if sq * sq == p - k3:
            r += 1
        k += 1
        k3 = k * k * k
    return r == 4

def solve():
    # to go faster, we actually generate the palindromes...
    n = 0
    r = 0
    l10 = 1
    h10 = 10
    while True:
        for prefix in range(l10, h10):
            p = genPal(h10, prefix, True)
            if check(p):
                print p
                n += 1
                r += p
                if n == 5:
                    return r
        for prefix in range(l10, h10):
            p = genPal(h10, prefix, False)
            if check(p):
                print p
                n += 1
                r += p
                if n == 5:
                    return r
        l10 *= 10
        h10 *= 10

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
