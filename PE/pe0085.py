def solve():
    # for an mxn grid, there are:
    # m(m+1)n(n+1)/4 rectangles
    r = 0
    mb = 0
    nb = 0
    for m in range(1, 2001):
        # we look, by bisection, for nL such that:
        # m(m+1)nL(nL+1)/4 < 2000000 < m(m+1)(nL+1)(nL+2)/4
        nL = 1
        nU = 2001
        while nU - nL > 1:
            nM = (nL+nU) / 2
            if m*(m+1)*nM*(nM+1)/4 < 2000000:
                nL = nM
            else:
                nU = nM
        vL = m*(m+1)*nL*(nL+1)/4
        vU = m*(m+1)*nU*(nU+1)/4
        if abs(2000000 - vL) < abs(2000000 - r):
            r = vL
            mb = m
            nb = nL
        if abs(2000000 - vU) < abs(2000000 - r):
            r = vU
            mb = m
            nb = nU
    return mb * nb


if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

