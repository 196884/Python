def solve():
    # Using the pentagonal number theorem
    b = 10000
    m = 10 ** 6
    p = [ 1, 1 ]
    n = 2
    while True:
        acc = 0
        k = 1
        sk = 1
        while k * (3 * k - 1) / 2 <= n:
            kp = k * (3*k+1) / 2
            km = k * (3*k-1) / 2
            np = n - kp
            nm = n - km
            if np >= 0:
                acc += sk * p[np]
            if nm >= 0:
                acc += sk * p[nm]
            acc = acc % m
            k   += 1
            sk  *= -1
        if acc == 0:
            return n
        p.append(acc)
        n += 1

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
