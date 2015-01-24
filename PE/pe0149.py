def genGrid():
    l = [(((100003 - 200003 * k + 300007 * k ** 3) % 1000000 ) - 500000) for k in range(1, 56)]
    for k in range(55, 4000000):
        l.append(((l[k-24] + l[k-55] + 1000000) % 1000000) - 500000)
    print l[9]
    print l[99]
    return l

def maxSumSubseq(l):
    r = 0
    c = 0
    for x in l:
        a = c + x
        if a < 0:
            c = 0
        else:
            c = a
            r = max(r, c)
    return r

def solve():
    g = genGrid()
    n = 2000
    r = 0
    for i in range(0, n):
        # lines
        l = [g[i + n * j] for j in range(0, n)]
        r = max(r, maxSumSubseq(l))
        # columns
        l = [g[n * i + j] for j in range(0, n)]
        r = max(r, maxSumSubseq(l))
        # SE diags from top
        l = [g[i + j + n * j] for j in range(0, n-i)]
        r = max(r, maxSumSubseq(l))
        # SE diags from left
        l = [g[j + (i + j) * n] for j in range(0, n-i)]
        r = max(r, maxSumSubseq(l))
        # SW diags from left
        l = [g[j + (i - j) * n] for j in range(0, i+1)]
        r = max(r, maxSumSubseq(l))
        # SW diags from bottom
        l = [g[i + j + (n - 1 - j) * n] for j in range(0, n-i)]
        r = max(r, maxSumSubseq(l))
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
