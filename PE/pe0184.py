def gcd(a, b):
    if b > a:
        return gcd(b, a)
    if b == 0:
        return a
    return gcd(b, a%b)

def cmpRad(((p1, q1), n1), ((p2, q2), n2)):
    return cmp(p1*q2, p2*q1)

def genRadiuses(rMax):
    d = dict()
    # we key them by (p, q) such that p/q = y/x (reduced)
    rMax2 = rMax ** 2
    for x in range(1, rMax):
        x2 = x ** 2
        y = 1
        while x2 + y * y < rMax2:
            g = gcd(x, y)
            p = y / g
            q = x / g
            n = d.get((p,q), 0)
            d[(p,q)] = n + 1
            y += 1
    # We add the ones for which y < 0:
    d2 = dict(d)
    for (p, q), n in d.iteritems():
        d2[(-p, q)] = n
    # We add the ones for which y = 0:
    d2[(0, 1)] = rMax - 1
    l = []
    for (p, q), n in d2.iteritems():
        l.append(((p, q), n))
    l.sort(cmpRad)
    r = [ rMax - 1 ]
    for x in l:
        r.append(x[1])
    return r

def solve():
    # We use the fact that we want the origin *strictly within* the triangle, so if we
    # consider the line L defined by x=0, there cannot be 2 vertices on L, so we'll partition
    # the cases between:
    # * 2 points with x < 0, 1 point with x > 0
    # * 2 points with x > 0, 1 point with x < 0 (same number of solutions as above)
    # * 1 point with x < 0, 1 point with x > 0, 1 point with x = 0
    # 
    # Now, we can also partition the points for which x > 0 as:
    # r1, r2, ..., r_N
    # where the points of ri are of the form:
    # l_j ( cos ai, sin ai )
    # (so they're all on a radius that makes an angle ai with the line L),
    # and a1 < a2 < ... < aN
    #
    # If we want to count the number of solutions for which 2 points have x > 0,
    # we can use the fact that 2 vertices cannot be on the same ri, and that the number of
    # solutions with a point on ri and another on rj (i < j) is:
    # Card(ri).Card(rj).\sum _{i<k<j}Card(rk)
    #
    # We can use the same kind of argument for the remaining of the points
    r = genRadiuses(105)
    N = len(r)
    # the first and last correspond to points with x = 0...
    result = 0
    for i in range(0, N):
        s = 0
        for j in range(i+1, N):
            result += 2 * r[i] * r[j] * s
            s += r[j]
    return result

if __name__ == "__main__":
    result = solve()
    print "Result: %s" % result
