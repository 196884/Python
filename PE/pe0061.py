def nextPerm(l):
    n = len(l)
    i = n - 1
    while i > 0 and l[i-1] >= l[i]:
        i -= 1
    if i <= 0:
        return list(reversed(l))
    j = n - 1
    while l[j] <= l[i-1]:
        j -= 1
    tmp = l[i-1]
    l[i-1] = l[j]
    l[j] = tmp
    j = n - 1
    while i < j:
        tmp = l[i]
        l[i] = l[j]
        l[j] = tmp
        i += 1
        j -= 1
    return l

def solve():
    # Pretty naive (small enough that it should work)
    s3 = []
    s4 = []
    s5 = []
    s6 = []
    s7 = []
    s8 = []
    for n in range(0, 150):
        n3 = n * (n+1) / 2
        n4 = n * n
        n5 = n * (3*n-1)/2
        n6 = n * (2*n-1)
        n7 = n * (5*n-3)/2
        n8 = n * (3*n-2)
        if n3 >= 1000 and n3 < 10000:
            s3.append(n3)
        if n4 >= 1000 and n4 < 10000:
            s4.append(n4)
        if n5 >= 1000 and n5 < 10000:
            s5.append(n5)
        if n6 >= 1000 and n6 < 10000:
            s6.append(n6)
        if n7 >= 1000 and n7 < 10000:
            s7.append(n7)
        if n8 >= 1000 and n8 < 10000:
            s8.append(n8)
    full = [s3, s4, s5, s6, s7, s8]
    byPrefix = []
    bySuffix = []
    for f in full:
        bp = [[] for i in range(0, 100)]
        bs = [[] for i in range(0, 100)]
        for n in f:
            bp[n/100].append(n)
            bs[n%100].append(n)
        byPrefix.append(bp)
        bySuffix.append(bs)

    cycle = [0, 1, 2, 3, 4]
    while True:
        l = [full[5], full[cycle[0]], full[cycle[1]], full[cycle[2]], full[cycle[3]], full[cycle[4]]]
        bp = [byPrefix[5], byPrefix[cycle[0]], byPrefix[cycle[1]], byPrefix[cycle[2]], byPrefix[cycle[3]], byPrefix[cycle[4]]]
        bs = [bySuffix[5], bySuffix[cycle[0]], bySuffix[cycle[1]], bySuffix[cycle[2]], bySuffix[cycle[3]], bySuffix[cycle[4]]]
   
        for n0 in l[0]:
            s0 = n0 % 100
            for n1 in bp[1][s0]:
                s1 = n1 % 100
                for n2 in bp[2][s1]:
                    s2 = n2 % 100
                    for n3 in bp[3][s2]:
                        s3 = n3 % 100
                        for n4 in bp[4][s3]:
                            s4 = n4 % 100
                            for n5 in bp[5][s4]:
                                s5 = n5 % 100
                                if n5 % 100 == n0 / 100:
                                    return n0+n1+n2+n3+n4+n5


        cycle = nextPerm(cycle)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
