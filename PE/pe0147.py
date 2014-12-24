def count(M, N, addRight = False):
    # not optimal: could get closed forms, but this works
    r = 0
    a = 1
    while 2 * M >= a:
        aL = a / 2
        aU = (a + 1) / 2
        b  = 1
        while 2 * (M - aL) >= b:
            bL = b / 2
            bU = (b + 1) / 2
            abU1 = (a + b + 1) / 2
            abU2 = (a + b + 2) / 2
            if M + 1 > aU + bU and N + 1 > abU1:
                r += (M+1-aU-bU) * (N+1-abU1)
            if M > aL + bL and N + 1 > abU2:
                r += (M-aL-bL) * (N+1-abU2)
            b += 1
        a+=1
    if addRight:
        r += M*(M+1)*N*(N+1)/4
    return r

def solve():
    r = 0
    for m in range(1, 48):
        for n in range(1, 44):
            r += count(m, n, True)
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
