import math as math

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

def powFloat(a, b, p):
    r = p
    a2k = a
    while b > 0:
        if b % 2 == 1:
            r = (r * a2k) / p
        a2k = (a2k * a2k) / p
        b /= 2
    return r

def solve():
    # We determine the set of n <= B such that F_n mod 10^10 is pandigital:
    B = 10000000
    fpp = 1
    fp = 1
    M = 10 ** 9
    prec = 10 ** 30
    r5 = iSqrt(5 * prec * prec )
    phi = ( r5 + prec ) / 2
    p1 = [ str(i) for i in range(1, 10) ]
    for n in range(3, B+1):
        f = (fp + fpp) % M
        fs = list(str(f))
        fs.sort()
        if fs == p1:
            print n
            y = powFloat(phi, n, prec)
            z = y / r5
            zs = list(str(z))
            zs = zs[:9]
            zs.sort()
            if zs == p1:
                return n
        fpp = fp
        fp = f
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %s" % result
