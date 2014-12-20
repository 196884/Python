for a in range(1, 999):
    n = 500000 - 1000 * a
    d = 1000 - a
    if n % d == 0:
        b = n / d
        if a < b:
            print "Result: %d" % (a * b * (1000 - a - b))
