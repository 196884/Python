def gcd(a, b):
    if a == b:
        return a
    if a < b:
        return gcd(b, a)
    if b == 0:
        return a
    return gcd(b, a%b)

def addFrac(n1, d1, n2, d2):
    n = n1 * d2 + n2 * d1
    d = d1 * d2
    g = gcd(abs(d), abs(n))
    return (n/g, d/g)

def interpolate(l):
    # if l contains n values,
    # assumes l = [P(1), P(2),..., P(n)] with P of degree n-1
    # and returns P(n+1)
    n = len(l)
    num = 0
    den = 1
    for i, v in enumerate(l):
        na = v
        nd = 1
        for k in range(0, n):
            if k != i:
                na *= n + 1 - ( k + 1 )
                nd *= i - k
        (num, den) = addFrac(num, den, na, nd)
    return num / den

def eval(l, x):
    r = 0
    for c in reversed(l):
        r *= x 
        r += c
    return r

def solve():
    # simple polynomial interpolation...
    p = [1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1]
    d = len(p)
    l = [ eval(p, i + 1) for i in range(d) ]
    r = 0
    for k in range(0, d-1):
        r += interpolate(l[:-k-1])
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
