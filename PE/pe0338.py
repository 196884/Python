def sumFast(n, k, eStart, eBound):
    result = 0
    eL = eStart
    rL = n / (k * eL)
    while eL < eBound and rL > 0:
        dE = 1
        eA = eL
        eB = eL + dE
        rB = n / (k * eB)
        while rB == rL:
            dE *= 2
            eA = eB
            eB += dE
            rB = n / (k * eB)
        while eB - eA > 1:
            eM = (eA + eB) / 2
            rM = n / (k * eM)
            if rM == rL:
                eA = eM
            else:
                eB = eM
                rB = rM
        eH = min(eBound, eB)
        rH = rB
        result += (eH - eL) * rL
        rL = rH
        eL = eH
    return result

def solve():
    n      = 10**12
    r1     = n
    dL     = 0
    dH     = 0
    result = 0
    i      = 0
    while r1 > 0:
        dL = dH
        dH = n / r1
        r0 = r1
        r1 = n / (dH + 1)
        x = sumFast(n, dH,     2, dH + 1)
        s = sumFast(n, dH + 1, 2, dH + 1)
        i += 1
        if i % 10000 == 0:
            print (i, dH, r0, r1, r0 * r1, x, s)
        result += (r0 - 1) * r1 - x - s
        k = dH - dL - 1
        if k > 0:
            result += k * (r0 * (r0 - 1) - 2 * x)
    return result

if __name__ == "__main__":
    # Really slow (a few improvements are doable)
    result = solve()
    print "Result: %d" % result
