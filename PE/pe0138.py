def solve():
    r = 17
    s = (38, 17)
    for k in range(1, 12):
        s0 = 9 * s[0] + 20 * s[1]
        s1 = 4 * s[0] + 9 * s[1]
        s = (s0, s1)
        r += s1
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
