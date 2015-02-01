def solve():
    # We start by not caring about L:
    B = 30
    l = [ (1, 1, 1) ]
    for n in range(1, B+1):
        (l0, l1, l2) = l[-1]
        l.append((l0+l1, l0+l2, l0))
    # We consider all possible positions of the L:
    r = l[B][0]
    for k in range(0, B):
        # k before, B-k-1 after:
        r += l[k][0] * l[B-k-1][0]
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
