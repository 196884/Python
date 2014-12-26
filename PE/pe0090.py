def genDice(k, l):
    # l are the allowed digits
    # k the number of values we still need
    n = len(l)
    if n < k:
        return []
    if n == k:
        return [list(l)]
    tail     = l[-1]
    lWithout = genDice(k, l[:-1])
    lWithAux = []
    if k > 0:
        lWithAux = genDice(k-1, l[:-1])
    for lAux in lWithAux:
        lAux.append(tail)
        lWithout.append(lAux)
    return lWithout

def isAdmissible(d1, d2):
    s1 = set(d1)
    s2 = set(d2)
    if 6 in s1:
        s1.add(9)
    if 9 in s1:
        s1.add(6)
    if 6 in s2:
        s2.add(9)
    if 9 in s2:
        s2.add(6)
    for (x, y) in [ (0,1), (0,4), (0,9), (1,6), (2,5), (3,6), (4,9), (6,4), (8,1) ]:
        if not((x in s1 and y in s2 ) or (x in s2 and y in s1)):
            return False
    return True

def solve():
    # there are only 10! / (6! 4!) = 210 possibilities for a dice (we exclude 4 digits)
    # so we exhaust:
    result = 0
    digits = [i for i in range(0, 10)]
    choices = genDice(6, digits)
    for d1 in choices:
        for d2 in choices:
            if isAdmissible(d1, d2):
                result += 1
    return result / 2

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
