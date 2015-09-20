from fractions import Fraction

def bbsIter((s, n, m)):
    s = ( s * s ) % n
    return (s % m, (s, n, m))

def buildSegments():
    s = 290797
    n = 50515093
    m = 500
    r = []
    state = (s, n, m)
    for i in range(0, 5000):
        (x1, state) = bbsIter(state)
        (y1, state) = bbsIter(state)
        (x2, state) = bbsIter(state)
        (y2, state) = bbsIter(state)
        r.append(((x1, y1), (x2, y2)))
    return r

def getInter(((a, b), (c, d)), ((x, y), (z, t))):
    betaDenom = (d-b)*(z-x) - (c-a)*(t-y)
    if betaDenom == 0:
        return None
    beta = Fraction(a*d - b*c + (c-a)*y - (d-b)*x, betaDenom)
    if beta <= Fraction(0, 1) or beta >= Fraction(1, 1):
        return None
    #print "beta: %d/%d" % (beta.numerator, beta.denominator)
    rx = x + beta * (z - x)
    ry = y + beta * (t - y)
    if c != a:
        alpha = (rx - a) / (c - a)
    else:
        alpha = (ry - b) / (d - b)
    if alpha <= Fraction(0, 1) or alpha >= Fraction(1, 1):
        return None
    return (rx, ry)

def solve():
    # Brute force...
    l = buildSegments()
    r = []
    for i in range(0, 5000):
        s1 = l[i]
        print i
        for j in range(0, i):
            s2 = l[j]
            p = getInter(s1, s2)
            if p != None:
                r.append(p)
    s = set(r)
    return len(s)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
