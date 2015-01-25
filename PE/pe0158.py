def fact(n):
    r = 1
    while n > 0:
        r *= n
        n -= 1
    return r

def choose(n, k):
    if k < 0 or k > n:
        return 0
    r = fact(n) / (fact(k) * fact(n-k))
    return r

def solve():
    # pretty naive
    B = 26
    L = 3
    n = [0 for l in range(0, B+1)]
    for a in range(0, B-1):
        nr = a
        for b in range(a+1, B):
            # a and b are going to be the inverted neighbors
            nm = b - a - 1
            nl = B - b - 1
            for r1 in range(0, nm + 1):
                for l2 in range(0, nm-r1 + 1):
                    for l1 in range(0, nl + 1):
                        for r2 in range(0, nr + 1):
                            n[2 + l1 + r1 + l2 + r2] += choose(nl, l1) * choose(nm, r1) * choose(nm - r1, l2) * choose(nr, r2)
    return max(n)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
