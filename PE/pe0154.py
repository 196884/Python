def iteratePascalTriangle(base, m):
    # n is the side length of the base, so we're building the one with side n+1
    n = len(base)
    r = [[1]]
    for a in range(1, n):
        nn = [(base[a-1][0] + base[a][0]) % m]
        for b in range(1, a):
            nn.append((base[a][b]+base[a-1][b]+base[a-1][b-1]) % m)
        nn.append(nn[0])
        r.append(nn)
    nn = []
    for b in range(0,n):
        nn.append(r[b][0])
    nn.append(1)
    r.append(nn)
    return r

def printPascalTriangle(l):
    for ll in l:
        s = ""
        for x in ll:
            if x == 0:
                s += "*"
            else:
                s += "_"
        print s

def genPascalTriangles(n, m):
    r = []
    l = [[1]]
    r.append(l)
    for k in range(1, n):
        l2 = iteratePascalTriangle(l, m)
        acc = 0
        for x in l2:
            for i in x:
                if i % m == 0:
                    acc += 1
        r.append(l2)
        l = l2
        print "k[%d] a[%d]" % (k, acc)
        if k % 5 == 0:
            printPascalTriangle(l)

def multiplesInFact(d, n):
    # Returns the largest power of d the divides n!
    r = 0
    dPow = d
    rr = n / dPow
    while rr > 0:
        r += rr
        dPow *= d
        rr = n / dPow
    return r

def solve():
    # naive and slow...
    n = 200000
    a2 = []
    a5 = []
    k1Bound = n / 3
    for k in range(n+1):
        a2.append( multiplesInFact(2, k) )
        a5.append( multiplesInFact(5, k) )
    b2 = a2[n] - 12
    b5 = a5[n] - 12
    r = 0
    for k1 in range(k1Bound + 1):
        k1_2 = a2[k1]
        k1_5 = a5[k1]
        k3   = n - 2 * k1
        if 2 * k1_2 + a2[k3] <= b2 and 2 * k1_5 + a5[k3] <= b5:
            r += 3
        if k1 % 2 == 0:
            k3 = ( n - k1 ) / 2
            if k1_2 + 2 * a2[k3] <= b2 and k1_5 + 2 * a5[k3] <= b5:
                r += 3
        k12 = 1
        k12Bound = n - 3 * k1
        while 2 * k12 < k12Bound:
            k2 = k1 + k12
            k3 = n - k1 - k2
            if k3 >= 0 and ( k1_2 + a2[k2] + a2[k3] ) <= b2 and ( k1_5 + a5[k2] + a5[k3] ) <= b5:
                r += 6
            k12 += 1
        print k1
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
