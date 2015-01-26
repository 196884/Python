B = 10 ** 99

cache = dict()
seen = set()

def check(n):
    while n > 0:
        if n % 10 > 2:
            return False
        n /= 10
    return True

def findMult(n, lc, p10):
    minD = 0
    if p10 == 1:
        minD = 1
    lr = []
    toAdd = dict()
    for (m, c) in lc:
        if check(c) and minD == 0:
            lr.append(m)
        else:
            for d in range(minD, 10):
                r = d * n + c
                if r % 10 < 3:
                    c2 = r / 10
                    m2 = p10 * d + m
                    k = (n, c2)
                    ta = toAdd.get(k, B)
                    toAdd[k] = min(ta, m2)
    if len(lr) > 0:
        return min(lr)
    lc2 = []
    for (n2, c2), m2 in toAdd.iteritems():
        if (n2, c2) not in seen:
            lc2.append((m2, c2))
            seen.add((n2, c2))
    return findMult(n, lc2, 10 * p10)

def solve():
    # not so complicated, but took a while to cache the right things...
    r = 0
    for n in range(1, 10001):
        x = findMult(n, [(0, 0)], 1)
        r += x
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
