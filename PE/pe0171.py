def fact(n):
    if n <= 1:
        return 1
    return n * fact(n-1)

def solve():
    targets = []
    n = 1
    while n * n <= 20 * 81:
        targets.append(n * n)
        n += 1
    targets = set( targets )
    facts = []
    for n in range(0, 21):
        facts.append( fact(n) )
    mult = 111111111
    m = 10**9
    r = 0

    n9 = 0
    s9 = 0
    r9 = 20
    while r9 >= 0:
        n8 = 0
        s8 = s9
        r8 = r9
        while r8 >= 0 and n8 <= r9:
            n7 = 0
            s7 = s8
            r7 = r8
            while r7 >= 0 and n7 <= r8:
                n6 = 0
                s6 = s7
                r6 = r7
                while r6 >= 0 and n6 <= r7:
                    n5 = 0
                    s5 = s6
                    r5 = r6
                    while r5 >= 0 and n5 <= r6:
                        n4 = 0
                        s4 = s5
                        r4 = r5
                        while r4 >= 0 and n4 <= r5:
                            n3 = 0
                            s3 = s4
                            r3 = r4
                            while r3 >= 0 and n3 <= r4:
                                n2 = 0
                                s2 = s3
                                r2 = r3
                                while r2 >= 0 and n2 <= r3:
                                    n1 = 0
                                    s1 = s2
                                    r1 = r2
                                    while r1 >= 0 and n1 <= r2:
                                        n0 = r1
                                        c = [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9]
                                        if s1 in targets:
                                            denom = 1
                                            for x in c:
                                                denom = denom * facts[x]
                                            for d in range(0, 10):
                                                if c[d] > 0:
                                                    r = ( r + d * mult * c[d] * facts[19] / denom ) % m
                                        n1 += 1
                                        s1 += 1
                                        r1 -= 1
                                    n2 += 1
                                    s2 += 4
                                    r2 -= 1
                                n3 += 1
                                s3 += 9
                                r3 -= 1
                            n4 += 1
                            s4 += 16
                            r4 -= 1
                        n5 += 1
                        s5 += 25
                        r5 -= 1
                    n6 += 1
                    s6 += 36
                    r6 -= 1
                n7 += 1
                s7 += 49
                r7 -= 1
            n8 += 1
            s8 += 64
            r8 -= 1
        n9 += 1
        s9 += 81
        r9 -= 1
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
