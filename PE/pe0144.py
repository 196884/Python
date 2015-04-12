# Bruteforcing it...

def iterate((x0, y0), (x1, y1)):
    num = 16 * x1 ** 2 * x0 + 8 * x1 * y0 * y1 -x0 * y1 ** 2 - 6 * x1 * y1 ** 2
    den = y1 ** 2 + 16 * x1 ** 2
    xs  = num / den
    ys  = y0 + 4 * x1 * ( x0 - xs ) / y1
    nl  = 8 * x1 * ( x1 - xs ) + 2 * y1 * ( y1 - ys )
    dl  = 4 * ( x1 - xs ) ** 2 + ( y1 - ys ) ** 2
    l   = nl / dl
    x2  = x1 + l * ( xs - x1 )
    y2  = y1 + l * ( ys - y1 )
    return (x2, y2)

def solve():
    (x0, y0) = (0, 10.1)
    (x1, y1) = (1.4, -9.6)
    r = 0
    while True:
        if y1 > 0 and abs(x1) <= 0.01:
            return r
        r += 1
        (x2, y2) = iterate((x0, y0), (x1, y1))
        (x0, y0) = (x1, y1)
        (x1, y1) = (x2, y2)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
