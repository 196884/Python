def nFromPos(l, a, i):
    """
    From (layer, angle, index):
    * layer is 0 a the center
    * angle from 0 to 5
    * index from 0 to layer-1
    """
    if l == 0:
        return 1
    if i == l:
        a = (a + 1) % 6
        i = 0
    return 2 + 6 * l * (l - 1) / 2 + a * l + i

def getNeighbors(l, a, i):
    # We basically distinguish the corner case
    # from the generic 'side' case
    if 0 == i:
        r = [(l, a, 1), (l, (a-1) % 6, l-1), (l-1, a, 0), (l+1, a, 0), (l+1, a, 1), (l+1, (a-1) % 6, l)]
    else:
        r = [(l, a, i+1), (l, a, i-1), (l-1, a, i-1), (l-1, a, i), (l+1, a, i), (l+1, a, i+1)]
    return r

def solve():
    B = 10000000
    primes = [True for i in range(0, B+1)]
    primes[0] = False
    primes[1] = False
    for n in range(2, B+1):
        if primes[n]:
            # n is prime
            kn = 2 * n
            while kn <= B:
                primes[kn] = False
                kn += n

    r = 1
    l = 1
    while True:
        # 2 possible cases:
        # (l, 0, 0) and
        # (l, 5, l-1)
        for (a, i) in [(0, 0), (5, l-1)]:
            n = nFromPos(l, a, i)
            ll = getNeighbors(l, a, i)
            lll = [nFromPos(x, y, z) for (x, y, z) in ll]
            c = 0
            for x in lll:
                t = abs(n - x)
                if primes[t]:
                    c += 1
            if 3 == c:
                r += 1
                if 2000 == r:
                    return n
        l += 1
    return 0


if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
