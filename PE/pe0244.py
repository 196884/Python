t16 = 2 ** 16

maxState = 2 ** 20

def checksumNext(cs, d):
    m = 100000007
    asciiValues = [ 76, 82, 85, 68 ]
    return ( cs * 243 + asciiValues[ d ] ) % m

def emptyPos(c):
    c = c / t16
    return (c / 4, c % 4)

def apply(state, mv):
    if state == 0:
        return 0
    (ei, ej) = emptyPos(state)
    if ( mv == 0 and ej == 3 ) or ( mv == 1 and ej == 0 ) or ( mv == 2 and ei == 3 ) or ( mv == 3 and ei == 0 ):
        return 0
    de = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    (dei, dej) = de[mv]
    nei = ei + dei
    nej = ej + dej
    # the empty is moving from (ei, ej) to (nei, nej)
    newState = state % t16
    # if needed, we update the color
    oldMask = 2 ** (4 * nei + nej)
    if state & oldMask:
        newState -= oldMask
        newState += 2 ** (4 * ei + ej)
    newState += t16 * (4 * nei + nej)
    return newState

def display(c):
    print "***********************"
    (ei, ej) = emptyPos(c)
    for i in range(0, 4):
        line = ""
        for j in range(0, 4):
            isRed = c & 2 ** (4 * i + j)
            if i == ei and j == ej:
                line += "E"
            else:
                if isRed:
                    line += "R"
                else:
                    line += "B"
        print line

def solve():
    s = 2 ** 1 + 2 ** 4 + 2 ** 5 + 2 ** 8 + 2 ** 9 + 2 ** 12 + 2 ** 13
    t = 2 ** 2 + 2 ** 5 + 2 ** 7 + 2 ** 8 + 2 ** 10 + 2 ** 13 + 2 ** 15
    d = dict()
    d[s] = [0]
    seen = set([0, s])
    r = 0
    nbIters = 0
    while True:
        dNew = dict()
        for state, lcs in d.iteritems():
            for mv in [0, 1, 2, 3]:
                stateNew = apply(state, mv)
                if stateNew not in seen:
                    l = dNew.get(stateNew, [])
                    for cs in lcs:
                        csNew = checksumNext(cs, mv)
                        if stateNew == t:
                            r += csNew
                        else:
                            l.append(csNew)
                            dNew[stateNew] = l
        if r > 0:
            return r
        d = dNew
        for k, v in d.iteritems():
            seen.add(k)
        print (nbIters, len(d))

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
