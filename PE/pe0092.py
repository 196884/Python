cache = dict()

def foo(n):
    if n == 89:
        return True
    if n == 1:
        return False
    r = cache.get(n, None)
    if r != None:
        return r
    a = 0
    na = n
    while na > 0:
        d = na % 10
        a += d * d
        na /= 10
    r = foo(a)
    cache[n] = r
    return r 

def solve():
    # Too lazy to optimize
    r = 0
    for k in range(1, 10000000):
        if foo(k):
            r += 1
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
