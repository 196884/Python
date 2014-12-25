def getkMax(a, N):
    kL = 1
    kU = (a - 1) / 2
    if 4 * kU * ( a - kU ) <= N:
        return kU
    # Dichotomy
    while kU - kL > 1:
        kM = (kL + kU) / 2
        if 4 * kM * ( a - kM ) > N:
            kU = kM
        else:
            kL = kM
    return kL

def solve():
    # Pretty naive, based on pe0173
    N = 1000000
    ways = [0 for i in range(0, N+1)]
    for a in range(3, N / 4 + 2):
        # a is the side of the large square
        # the small side is then of size b = a - 2*k, with the following constraints:
        # * k >= 1
        # * k <= (a-1) / 2
        # * a^2 - b^2 <= N i.e., 4k^2 - 4ak + N >= 0
        #   i.e., k <= ( a - Sqrt(a^2-N) ) / 2
        kMax = getkMax(a, N)
        for k in range(1, kMax+1):
            ways[a*a - (a-2*k)*(a-2*k)] += 1
    r = 0
    for x in ways:
        if x > 0 and x <= 10:
            r += 1
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
