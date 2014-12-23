# T(2n-1)=H(n), so we just need to find a number both
# pentagonal and hexagonal

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

def isPen(n):
    r = (1 + 24*n)
    s = iSqrt(r)
    if s * s != r:
        return False
    return s % 6 == 5

def solve():
    n = 143
    while True:
        n += 1
        Hn = n * ( 2 * n - 1 )
        if isPen(Hn):
            return Hn


if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
