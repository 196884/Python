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
    N = 1000000
    r = 0
    kMin = 1
    for a in range(3, N / 4 + 2):
        # a is the side of the large square
        # the small side is then of size b = a - 2*k, with the following constraints:
        # * k >= 1
        # * k <= (a-1) / 2
        # * a^2 - b^2 <= N i.e., 4k^2 - 4ak + N >= 0
        #   i.e., k <= ( a - Sqrt(a^2-N) ) / 2
        kMax = getkMax(a, N)
        r += kMax 
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
