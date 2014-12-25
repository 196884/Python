def nbDigits(n):
    r = 0
    while n > 0:
        n /= 10
        r += 1
    return r

def solve():
    r = 0
    n = 1
    d = 2
    for k in range(1, 1000):
        aux = d
        d = 2 * d + n
        n = aux
        if nbDigits(d+n) > nbDigits(d):
            r += 1
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

