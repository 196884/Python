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

def solve():
    # We use the parametrization of Pythagorean triplets:
    LMax = 10 ** 8
    r = 0
    m = 2
    m2 = m * m
    while 2 * m2 <= LMax:
        for e in [-1, 1]:
            aux = 2 * m2 + e
            raux = iSqrt(aux)
            if raux * raux == aux:
                n = raux - m
                l = 2 * m * (m + n)
                r += LMax / l
        m += 1
        m2 = m * m
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
