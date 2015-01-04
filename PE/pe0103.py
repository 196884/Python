cacheSum = dict()

def testSet1(l, x):
    n = len(l)
    b = 2 ** n
    for k1 in range(0, b):
        # we split [0..n-1] between the indices encoded by k1 and the complement:
        sum1 = x
        c1 = []
        aux1 = k1
        for i, li in enumerate(l):
            if aux1 % 2 == 1:
                sum1 += li
            else:
                c1.append(li)
            aux1 /= 2
        nc1 = len(c1)
        bc1 = 2 ** nc1
        for k2 in range(0, bc1):
            sum2 = 0
            aux2 = k2
            for i, li in enumerate(c1):
                if aux2 % 2 == 1:
                    sum2 += li
                aux2 /= 2
            if sum1 == sum2:
                return False
    return True

def testSet2(l, x):
    n = len(l)
    if n == 0:
        return x > 0
    if x <= l[-1]:
        return False
    if n == 1:
        return True
    s1 = l[0] + l[1]
    s2 = x
    if s2 >= s1:
        return False
    i1 = 2
    i2 = n-1
    while i1 < i2:
        s1 += l[i1]
        s2 += l[i2]
        if s2 >= s1:
            return False
        i1 += 1
        i2 -= 1
    return True

def setsForSum(s, n):
    r = cacheSum.get((s, n), None)
    if None != r:
        return r
    if n == 0 or s <= 0:
        return []
    if n == 1:
        return [ [s] ]
    r = []
    for k in range(1, s-1):
        subsets = setsForSum(s-k, n-1)
        for ss in subsets:
            if testSet2(ss, k) and testSet1(ss, k):
                rr = list(ss)
                rr.append(k)
                r.append(rr)
    cacheSum[(s, n)] = r
    return r

def solve():
    # Very naive, and quite slow...
    k = 110
    while True:
        a = setsForSum(k, 7)
        if len(a):
            x = a[0]
            s = ""
            for i in x:
                s = "%s%d" % (s, i)
            return int(s)
        k += 1

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
