def iter(n):
    f = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]
    r = 0
    while n > 0:
        r += f[n%10]
        n /= 10
    return r

def check(n):
    k = n
    s = set()
    for i in range(0, 61):
        s.add(k)
        k = iter(k)
    return len(s) == 60

def solve():
    # Naive and slow, could easily optimize by caching more
    cache = {1: 1, 2: 1, 145: 1, 169: 3, 871: 2, 872: 2, 40585: 1}
    toCheck = []
    for k in range(1, 1000000):
        kk = k
        lk = []
        ok = True
        n = 1
        i = 0
        while ok and i < 60:
            lk.append(kk)
            cached = cache.get(kk, 0)

            if cached > 0:
                if i + cached >= 60:
                    toCheck.append(k)
                #print "k: %d, i: %d, cached: %d" % (k, i, cached)
                #print lk
                ok = False

            kk = iter(kk)
            i += 1
        if ok:
            toCheck.append(k)
    result = 0
    for n in toCheck:
        if check(n):
            result += 1
    return result

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
