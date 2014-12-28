def iterFareyFast(x, bound):
    (n, l) = x
    # n is the separate count
    # l is a list of lists...
    r = []
    for ll in l:
        if len(ll) == 1:
            n += 1
        else:
            rr = []
            prev = None
            for (a, b) in ll:
                if prev == None:
                    rr.append((a, b))
                    prev = (a, b)
                else:
                    aa = a+prev[0]
                    bb = b+prev[1]
                    if bb <= bound:
                        rr.append((aa, bb))
                        rr.append((a, b))
                        prev = (a, b)
                    else:
                        r.append(rr)
                        rr = [(a, b)]
                        prev = (a, b)
            r.append(rr)
    return (n, r)

def solve():
    # Slow again... b/c we do a full computation of the Farey sequence via the medians and early pruning
    n = 12000
    l = [(1, 3), (1, 2)]
    x = (0, [l])
    done = False
    while not done:
        x = iterFareyFast(x, n)
        done = len(x[1]) == 0
    return x[0] - 2

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
