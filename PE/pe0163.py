from fractions import Fraction
import itertools

def getInter(((a, b), (c, d)), ((x, y), (z, t))):
    betaDenom = (d-b)*(z-x) - (c-a)*(t-y)
    if betaDenom == 0:
        return None
    beta = Fraction(a*d - b*c + (c-a)*y - (d-b)*x, betaDenom)
    if beta <= Fraction(0, 1) or beta >= Fraction(1, 1):
        return None
    rx = x + beta * (z - x)
    ry = y + beta * (t - y)
    if c != a:
        alpha = (rx - a) / (c - a)
    else:
        alpha = (ry - b) / (d - b)
    if alpha <= Fraction(0, 1) or alpha >= Fraction(1, 1):
        return None
    return (rx, ry)

def add3(x, y):
    return (x[0] + y[0], x[1] + y[1])

def sub3(x, y):
    return (x[0] - y[0], x[1] - y[1])

def mul3(x, y):
    return (x[0] * y[0] + 3 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])

def norm3(x):
    return x[0]**2 - 3 * x[1]**2

def conj3(x):
    return (x[0], -x[1])

def inv3(x):
    n3 = norm3(x)
    return (x[0]/n3, -x[1]/n3)

def div3(x, y):
    return mul3(x, inv3(y))

def isZero3(x):
    return x[0].numerator == 0 and x[1].numerator == 0

def geq0_3((a, b)):
    if a >= 0:
        if b >= 0:
            return True
        return a * a >= 3 * b * b
    else:
        # a < 0
        if b >= 0:
            return 3 * b * b >= a * a
        return False

def inBounds3((a, b)):
    return geq0_3((a, b)) and geq0_3((1-a, -b))

def pointsWA(p1, p2, w):
    # (1-w) p1 + w p2
    (p1x, p1y) = p1
    (p2x, p2y) = p2
    c1 = (Fraction(1, 1) - w, Fraction(0, 1))
    c2 = (w, Fraction(0, 1))
    return (add3(mul3(c1, p1x), mul3(c2, p2x)), add3(mul3(c1, p1y), mul3(c2, p2y)))

def createLines(s1, s2):
    if len(s1) != len(s2):
        return None
    r = []
    for i, P1 in enumerate(s1):
        P2 = s2[i]
        r.append((P1, P2))
    return r

def intersection(((a, b), (c, d)), ((x, y), (z, t))):
    if (a, b) == (c, d) or (x, y) == (z, t):
        return None
    betaDenom = sub3(mul3(sub3(d, b), sub3(z, x)), mul3(sub3(c, a), sub3(t, y)))
    betaNum   = add3( sub3( mul3(a, d), mul3(b, c) ), sub3( mul3( sub3(c, a), y), mul3( sub3(d, b), x) ) )
    beta      = div3(betaNum, betaDenom)
    if not inBounds3(beta):
        return None
    rx = add3(x, mul3(beta, sub3(z, x)))
    ry = add3(y, mul3(beta, sub3(t, y)))
    return (rx, ry)

def countTriangles(l):
    r = 0
    count = 0
    n0 = len(l[0])
    for i0, line0 in enumerate(l[0]):
        print (i0, n0)
        for line1 in l[1]:
            inter01 = intersection( line0, line1 )
            if inter01 != None:
                for line2 in l[2]:
                    inter02 = intersection( line0, line2 )
                    if inter02 != None and inter02 != inter01:
                        inter12 = intersection( line1, line2 )
                        if inter12 != None and inter12 != inter01 and inter12 != inter02:
                            r += 1
    return r

def solve():
    # Stupid brute force, though a closed form should be doable
    n = 36
    P2 = ((Fraction(0, 1), Fraction(0, 1)), (Fraction(0, 1), Fraction(0, 1)))
    P1 = ((Fraction(n, 1), Fraction(0, 1)), (Fraction(0, 1), Fraction(0, 1)))
    P0 = ((Fraction(n, 2), Fraction(0, 1)), (Fraction(0, 1), Fraction(n, 2)))
    wF = [Fraction(k, n) for k in range(0, n+1)]
    wH = [Fraction(k, 2*n) for k in range(0, 2*n+1)]
    F0 = [pointsWA(P2, P1, w) for w in wF]
    F2 = [pointsWA(P1, P0, w) for w in wF]
    F1 = [pointsWA(P0, P2, w) for w in wF]
    H0 = [pointsWA(P2, P1, w) for w in wH]
    H2 = [pointsWA(P1, P0, w) for w in wH]
    H1 = [pointsWA(P0, P2, w) for w in wH]
    F0i = list(reversed(F0))
    F1i = list(reversed(F1))
    F2i = list(reversed(F2))
    A0 = F1i[:-1] + F2i
    A1 = F2i[:-1] + F0i
    A2 = F0i[:-1] + F1i
    # We start with the set of vertical lines:
    V0 = createLines(H0, A0)
    V1 = createLines(H1, A1)
    V2 = createLines(H2, A2)
    B0 = createLines(F1i, F2)
    B1 = createLines(F2i, F0)
    B2 = createLines(F0i, F1)
    allLines = [V0, V1, V2, B0, B1, B2]
    indices  = set([0, 1, 2, 3, 4, 5])
    triples = set(itertools.combinations(indices, 3))
    r = 0
    for s in triples:
        print s
        lines = [allLines[i] for i in s]
        r += countTriangles(lines)
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
