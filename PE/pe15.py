def solve():
    n = 20
    l = [1 for i in range(0, n+1)]
    for a in range(0, n):
        acc = 0
        lNew = []
        for b in range(0, n+1):
            acc += l[b]
            lNew.append(acc)
        l = lNew
    return l[-1]

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
