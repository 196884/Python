def gcd(a, b):
    if a == b:
        return a
    if a < b:
        return gcd(b, a)
    if b == 0:
        return a
    return gcd(b, a%b)

def abs(x):
    if x < 0:
        return -x
    return x

def red(n, d):
    g = gcd(abs(n), abs(d))
    if d < 0:
        n *= -1
        d *= -1
    return (n/g, d/g)

def applyOp(op, (na, da), (nb, db)):
    if op == 0:
        return red(na * db + nb * da, da * db)
    if op == 1:
        return red(na * db - nb * da, da * db)
    if op == 2:
        return red(na * nb, da * db)
    if op == 3:
        return red(na * db, da * nb)

perm4 = [
    [ 0, 1, 2, 3 ],
    [ 0, 1, 3, 2 ],
    [ 0, 2, 1, 3 ],
    [ 0, 2, 3, 1 ],
    [ 0, 3, 1, 2 ],
    [ 0, 3, 2, 1 ],
    [ 1, 0, 2, 3 ],
    [ 1, 0, 3, 2 ],
    [ 1, 2, 0, 3 ],
    [ 1, 2, 3, 0 ],
    [ 1, 3, 0, 2 ],
    [ 1, 3, 2, 0 ],
    [ 2, 0, 1, 3 ],
    [ 2, 0, 3, 1 ],
    [ 2, 1, 0, 3 ],
    [ 2, 1, 3, 0 ],
    [ 2, 3, 0, 1 ],
    [ 2, 3, 1, 0 ],
    [ 3, 0, 1, 2 ],
    [ 3, 0, 2, 1 ],
    [ 3, 1, 0, 2 ],
    [ 3, 1, 2, 0 ],
    [ 3, 2, 0, 1 ],
    [ 3, 2, 1, 0 ]
]

def evalAllTrees(digits):
    # digits is an array of 4 elements
    # there are basically 3 different binary trees with 4 leaves
    # and 4 possible operators for each of the 3 internal nodes
    l = []
    for op1 in range(0, 4):
        for op2 in range(0, 4):
            for op3 in range(0, 4):
                for p in perm4:
                    n0 = (digits[p[0]], 1)
                    n1 = (digits[p[1]], 1)
                    n2 = (digits[p[2]], 1)
                    n3 = (digits[p[3]], 1)
                    # first tree:
                    int1 = applyOp(op1, n0, n1)
                    int2 = applyOp(op2, n2, n3)
                    r    = applyOp(op3, int1, int2)
                    l.append(r)
                    # second tree:
                    int3 = applyOp(op2, int1, n2)
                    r    = applyOp(op3, int3, n3)
                    l.append(r)
                    # third tree:
                    int4 = applyOp(op2, n2, int2)
                    r    = applyOp(op3, n3, int4)
                    l.append(r)
    s = set()
    for (a, b) in l:
        if b == 1:
            s.add(a)
    r = 0
    while True:
        if (r+1) in s:
            r += 1
        else:
            return r

def genTuples(l, k):
    """
    Generates all k-tuples from l elements
    """
    if k == len(l):
        return [list(l)]
    if k > len(l):
        return []
    if k == 0:
        return [[]]
    # at this point, k < len(l)
    prefix = list(l[:-1])
    l1 = genTuples(prefix, k)
    l2 = genTuples(prefix, k-1)
    x  = l[-1]
    for y in l2:
        y.append(x)
        l1.append(y)
    return l1

def toInt(l):
    r = 0
    for x in l:
        r = 10 * r + x
    return r

def solve():
    allDigits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    allTuples = genTuples(allDigits, 4)
    maxV = 0
    maxT = []
    for t in allTuples:
        v = evalAllTrees(t)
        if v > maxV:
            maxV = v
            maxT = t
    return toInt(maxT)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
    
