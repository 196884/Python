def solve():
    # Using the pentagonal number theorem
    b = 100
    p = [ 1, 1 ]
    for n in range(2, b+1):
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
            k   += 1
            sk  *= -1
        p.append(acc)
    return p[-1] - 1

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
