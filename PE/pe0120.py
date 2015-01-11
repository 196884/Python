def solve():
    r = 0
    for a in range(3, 1001):
        a2 = a * a
        m = 0
        for n in range(1, a):
            x = (2 * n * a) % a2
            m = max(x, m)
        r += m
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
