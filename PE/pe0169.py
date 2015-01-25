cache = dict()
cache[1] = 1
cache[2] = 2

def f(n):
    cached = cache.get(n, None)
    if cached != None:
        return cached
    if n % 2 == 1:
        r = f(n / 2)
    else:
        r = f(n / 2) + f(n / 2 - 1)
    cache[n] = r
    return r

def solve():
    # Simple recursion with memoization
    return f(10**25)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
