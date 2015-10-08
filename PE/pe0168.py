def solve():
    r = 0
    m = 10**5
    for k in range(1, 100):
        mk = 10**(k+1) - 1
        for d0 in range(1, 10):
            mkd0 = d0 * mk
            for a in range(1, 10):
                if mkd0 % (10 * a - 1) == 0:
                    n = mkd0 / (10 * a - 1)
                    if n >= 10**k:
                        r = (r + n) % m
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
