def solve():
    # not particularly proud...
    l4 = [0 for i in range(0, 37)]
    l6 = [0 for i in range(0, 37)]
    for d1 in range(1, 5):
        for d2 in range(1, 5):
            s2 = d1 + d2
            for d3 in range(1, 5):
                s3 = s2 + d3
                for d4 in range(1, 5):
                    s4 = s3 + d4
                    for d5 in range(1, 5):
                        s5 = s4 + d5
                        for d6 in range(1, 5):
                            s6 = s5 + d6
                            for d7 in range(1, 5):
                                s7 = s6 + d7
                                for d8 in range(1, 5):
                                    s8 = s7 + d8
                                    for d9 in range(1, 5):
                                        l4[s8 + d9] += 1
    for d1 in range(1, 7):
        for d2 in range(1, 7):
            s2 = d1 + d2
            for d3 in range(1, 7):
                s3 = s2 + d3
                for d4 in range(1, 7):
                    s4 = s3 + d4
                    for d5 in range(1, 7):
                        s5 = s4 + d5
                        for d6 in range(1, 7):
                            l6[s5 + d6] += 1
    n4 = float(sum(l4))
    n6 = float(sum(l6))
    r  = float(0)
    for i4, t4 in enumerate(l4):
        for i6, t6 in enumerate(l6):
            if i4 > i6:
                r += float( t4 * t6 ) / ( n4 * n6 )
    print r
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
