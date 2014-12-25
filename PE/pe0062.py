def normalize(n):
    l = []
    z = 0
    while n > 0:
        r = n % 10
        l.append(r)
        if r == 0:
            z += 1
        n /= 10
    l.sort()
    r = 0
    for x in l:
        r = 10 * r + x
    for i in range(0, z):
        r *= 10
    return r

def solve():
    n = 2
    cache = dict()
    while True:
        n3 = n * n * n
        k  = normalize(n3)
        (nb, l) = cache.get(k, (0, []))
        l.append(n)
        if nb >= 4:
            return l[0] ** 3
        if nb == 0:
            cache[k] = (1, l)
        else:
            cache[k] = (nb+1, l)
        n += 1

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
