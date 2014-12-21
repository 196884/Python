def foo(k):
    s = set()
    for i in range(2, 101):
        for j in range(1, k+1):
            s.add(i*j)
    return len(s)

def solve():
    r = 0
    done = set()
    for a in range(2, 101):
        if a not in done:
            # we get the max k such that a^k <= 100:
            ak = a
            k = 0
            while ak <= 100:
                done.add(ak)
                k += 1
                ak *= a
            r += foo(k)
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
