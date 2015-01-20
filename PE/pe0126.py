def solve():
    B = 20000
    l = [0 for i in range(0, B+1)]
    for a in range(1, B+1):
        b = 1
        while b <= a:
            s = a + b
            p = a * b
            cs = 2
            c0 = 0
            nl = cs * s + 2 * p + c0
            j  = 0
            while nl <= B:
                nls = nl
                c   = 1
                while nls <= B and c <= b:
                    l[ nls ] += 1
                    nls += 2 * s + 4 * j
                    c += 1
                c0 += 2 * cs
                cs += 4
                nl  = cs * s + 2 * p + c0
                j  += 1
            b += 1
    for i, j in enumerate(l):
        if j == 1000:
            return i
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
