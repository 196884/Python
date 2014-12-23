def pent(n):
    return n * (3*n-1) / 2

def solve():
    # Simple search works - wanted to find one to bound the solution, but one can prove this
    # is the actual min.
    b = 10000
    pList = [pent(n) for n in range(1, b)]
    pSet = set(pList)
    for p1 in pList:
        for p2 in pList:
            if p1+p2 in pSet and p1-p2 in pSet:
                return p1-p2
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
