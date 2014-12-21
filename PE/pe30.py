# Brute force:
# since 9^5*6 < 10^6, solutions have at most 6 digits

def solve():
    r = 0
    for d0 in range(0, 10):
        s0 = d0
        t0 = d0*d0*d0*d0*d0
        for d1 in range(0, 10):
            s1 = 10 * d1 + s0
            t1 = t0 + d1*d1*d1*d1*d1
            for d2 in range(0, 10):
                s2 = 100 * d2 + s1
                t2 = t1 + d2*d2*d2*d2*d2
                for d3 in range(0, 10):
                    s3 = 1000 * d3 + s2
                    t3 = t2 + d3*d3*d3*d3*d3
                    for d4 in range(0, 10):
                        s4 = 10000 * d4 + s3
                        t4 = t3 + d4*d4*d4*d4*d4
                        for d5 in range(0, 10):
                            s5 = 100000 * d5 + s4
                            t5 = t4 + d5*d5*d5*d5*d5
                            if s5 == t5:
                                r += s5
    return r - 1
            
if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
