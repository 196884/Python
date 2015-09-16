def solve():
    n = 10 ** 17
    l = [(1,1), (2,2)]
    last = 2
    while l[-1][0] < n:
        l.append((l[-1][0] + l[-2][0], l[-1][1] + l[-2][1] + l[-1][0]))
    r = 0
    c = False
    for (f, s) in reversed(l):
        if c:
            r += s
        if n >= f:
            r += n - f
            n -= f
            c = True
        else:
            c = False
    return r

if __name__ == "__main__":
    result = solve()
    print "result: %s" % result
