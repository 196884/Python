def solve():
    # We use the basic definition of the Pascal triangle, and its symmetry
    bound = 1000000 
    nMax = 100
    l = [1, 1]
    r = 0
    for n in range(2, nMax+1):
        prev = 0
        lNew = []
        i    = 0
        lSz  = len(l)
        done = False
        while i < lSz and not done:
            x = l[i] + prev
            if x >= bound:
                done = True
                r += n - 2 * i + 1
            else:
                prev = l[i]
            lNew.append(x)
            i += 1
        if not done:
            lNew.append(1)
        print lNew
        l = list(lNew)
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

