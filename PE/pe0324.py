import array

q = 100000007

def checkI(cfg, i, j):
    if i >= 2:
        return 0
    e0 = 2 ** (i + 3 * j)
    e1 = 2 ** (i + 1 + 3 * j)
    c = (cfg & e0) + (cfg & e1)
    if c > 0:
        return 0
    return cfg + e0 + e1

def checkJ(cfg, i, j):
    if j >= 2:
        return 0
    e0 = 2 ** (i + 3 * j)
    e1 = 2 ** (i + 3 * (j + 1))
    c = (cfg & e0) + (cfg & e1)
    if c > 0:
        return 0
    return cfg + e0 + e1

def countBase(i, j, cfg, d):
    if i > 3 or j > 3:
        return d
    if i == 3:
        return countBase(0, j+1, cfg, d)
    if j == 3:
        a = d.get(cfg, 0)
        d[cfg] = a+1
        return d
    d = countBase(i+1, j, cfg, d)
    cfgI = checkI(cfg, i, j)
    cfgJ = checkJ(cfg, i, j)
    if cfgI > 0:
        d = countBase(i, j, cfgI, d)
    if cfgJ > 0:
        d = countBase(i, j, cfgJ, d)
    return d

def buildD1():
    d = dict()
    d = countBase(0, 0, 0, d)
    r = []
    for i in range(0, 512):
        r.append(0)
    #r = array.array('i', (0 for i in range(0, 512)))
    for k, n in d.iteritems():
        r[k] = n
    return r

def buildD2(d1):
    r = array.array('i', (0 for i in range(0, 512 * 512)))
    for k in range(0, 512):
        for i in range(0, 512):
            if i & k == 0:
                for j in range(0, 512):
                    if j & k == 0:
                        r[ i + k + 512 * (j + k) ] += d1[i] * d1[j]
    return r

def buildDouble(s):
    r = array.array('i', (0 for i in range(0, 512 * 512)))
    for a in range(0, 512):
        for b in range(0, 512):
            aux = s[a + 512 * b]
            if aux > 0:
                for c in range(0, 512):
                    r[b + 512 * c] = (r[b + 512 * c] + aux * s[a + 512 * c]) % q
    return r

def add(s, t):
    r = array.array('i', (0 for i in range(0, 512 * 512)))
    for a in range(0, 512):
        for b in range(0, 512):
            aux = s[a + 512 * b]
            if aux > 0:
                for c in range(0, 512):
                    r[b + 512 * c] = (r[b + 512 * c] + aux * t[a + 512 * c]) % q
    return r

def matMatMult(a, b, q):
    n = len(a)
    r = []
    for i in range(0, n):
        rr = []
        for j in range(0, n):
            aux = 0
            for k in range(0, n):
                aux += a[i][k] * b[k][j]
                aux = aux % q
            rr.append(aux)
        r.append(rr)
    return r

def matPow(a, k, q):
    n = len(a)
    r = []
    for i in range(0, n):
        rr = []
        for j in range(0, n):
            rr.append(0)
        rr[i] = 1
        r.append(rr)
    bits = []
    while k > 0:
        bits.append(k % 2)
        k /= 2
    for b in reversed(bits):
        r = matMatMult(r, r, q)
        if b == 1:
            r = matMatMult(r, a, q)
    return r

def matVectMult0(a, b, q):
    r = 0
    n = len(a)
    for i in range(0, n):
        r += a[0][i] * b[i]
        r = r % q
    return r

def sol(coefs, v0, n):
    order = len( coefs )
    a = []
    for i in range(0, order-1):
        aa = []
        for j in range(0, order):
            aa.append(0)
        aa[i+1] = 1
        a.append(aa)
    a.append(list(reversed(coefs)))
    ap = matPow(a, n, q)
    return matVectMult0(ap, v0, q)
    

def solve():
    # After some investigating using the naive approach, one finds that the sequence
    # satisfies a linear recurrence:
    coefs = [ 679, -76177, 3519127, -85911555, 1235863045, -11123194131, 65256474997, -257866595482, 705239311926, -1363115167354, 1888426032982, -1888426032982, 1363115167354, -705239311926, 257866595482, -65256474997, 11123194131, -1235863045, 85911555, -3519127, 76177, -679, 1 ]
    order = len( coefs )
    a = []
    for i in range(0, order-1):
        aa = []
        for j in range(0, order):
            aa.append(0)
        aa[i+1] = 1
        a.append(aa)
    a.append(list(reversed(coefs)))
    v0 = [ 
        1,
        229,
        117805,
        64647289,
        35669566217,
        19690797527709,
        10870506600976757,
        6001202979497804657,
        3313042830624031354513,
        1829008840116358153050197,
        1009728374600381843221483965,
        557433823481589253332775648233,
        307738670509229621147710358375321,
        169891178715542584369273129260748045,
        93790658670253542024618689133882565125,
        51778366130057389441239986148841747669217,
        28584927722109981792301610403923348017948449,
        15780685138381102545287108197623881881376915397,
        8711934690116480171969789787256390490181022415693,
        4809538076408327645969201260680362259835079086427481,
        2655168723276120197512956906659822833388644760430125609,
        1465820799640802552047402979496052449322258430218930512765,
        809225642733724788155919446555896648357335949987871250500245
    ]
    return sol(coefs, v0, 5 * 10 ** 9999)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
