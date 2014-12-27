def solve():
    # We use a cache telling us if previous numbers were increasing or decreasing
    # best would be to do it the other way (add the first digit), as it would allow us
    # to skip much more... but this is good enough
    cache = [(True, True)]
    nbBouncy = 0
    n = 0
    while True:
        n += 1
        nl = n / 10
        nr = n % 10
        (nlInc, nlDec) = cache[nl]
        if nl == 0:
            cache.append((True, True))
        else:
            nInc = nlInc and nr >= (nl % 10)
            nDec = nlDec and nr <= (nl % 10)
            cache.append((nInc, nDec))
            if not (nInc or nDec):
                nbBouncy += 1
        if 100 * nbBouncy >= 99 * n:
            return n

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
