from fractions import Fraction


def solve():
    allDone = set()
    exact = dict()
    allDone.add(Fraction(1,1))
    exact[1] = set(allDone)
    N = 18
    for k in range(2, N+1):
        sk = set()
        for i in range(1, k):
            if 2 * i <= k:
                si = exact[i]
                sj = exact[k-i]
                for a in si:
                    for b in sj:
                        x = a + b
                        if x not in allDone:
                            allDone.add(x)
                            sk.add(x)
                        y = 1 / ( 1 / a + 1 / b )
                        if y not in allDone:
                            allDone.add(y)
                            sk.add(y)
        exact[k] = sk
        print "****************************"
        print "k[%d] (%d)" % (k, len(exact[k]))
    return len(allDone)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
