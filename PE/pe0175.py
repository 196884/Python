def toBinary(n):
    r = []
    while n > 0:
        r.append(n % 2)
        n /= 2
    return list(reversed(r))

def fromBinary(l):
    r = 0
    for x in l:
        r = 2 * r + x
    return r

def F(k):
    if k < 2:
        return 1
    if k % 2 == 1:
        return F(k/2)
    return F(k/2) + F(k/2-1)

def G(l):
    return F(fromBinary(l))

def A(l):
    r = []
    d = 1
    for x in l:
        for a in range(x):
            r.append(d)
        d = 1 - d
    return r

def Bc(l):
    return G(A(l))

def B(l):
    if len(l) % 2 == 1:
        l = l[:-1]
    s = (1, 1)
    for k in range(len(l)/2):
        e = l[2*k]
        f = l[2*k+1]
        s0 = f * s[1] + (1 + f * (e - 1) ) * s[0]
        s1 = (f+1) * s[1] + (1 + (f+1) * (e - 1) ) * s[0]
        s = (s0, s1)
    return s[0]

def gcd(a, b):
    if b == 0:
        return a
    if b > a:
        return gcd(b, a)
    return gcd(b, a % b)

def walkSBTree(p, q):
    # Slow, but good enough
    l = []
    bL = (0, 1)
    bH = (1, 0)
    bM = (bL[0] + bH[0], bL[1] + bH[1])
    while p * bM[1] != q * bM[0]:
        if p * bM[1] > q * bM[0]:
            l.append(0)
            bL = bM
        else:
            l.append(1)
            bH = bM
        bM = (bL[0] + bH[0], bL[1] + bH[1])
    l.append(1)
    return l

def solve():
    # We 'just' walk down the Stern-Brocot tree:
    # (First found some recursions, see above, and was trying to solve it backwards when I realized the Stern-Brocot pattern)
    l = walkSBTree(123456789, 987654321)
    r = []
    d = 0
    last = 0
    for x in l:
        if x == last:
            d += 1
        else:
            if d > 0:
                r.append(d)
                r.append(",")
            d = 1
            last = x
    r.append(d)
    n = ""
    for s in reversed(r):
        n += str(s)
    return n
if __name__ == "__main__":
    result = solve()
    print "Result: %s" % result
