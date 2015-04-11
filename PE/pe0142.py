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

def isSqr(n):
    if n <= 0:
        return False
    r = iSqrt(n)
    result = r * r == n
    return result

def solve():
    ra = 3
    while True:
        ra += 1
        a = ra * ra
        rc = 2
        while rc < ra:
            rc += 1
            c = rc * rc
            f = a - c
            if isSqr(f):
                rd = 1
                if (rc % 2 == 0):
                    rd += 1
                while rd < rc:
                    d = rd * rd
                    e = a - d
                    b = c - e
                    if isSqr(b) and isSqr(e):
                        result = c + (e + f) / 2
                        return result
                    rd += 2

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
