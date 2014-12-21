# 9! = 362880
# 10^7 > 8 * 9!
# so the number of digits is <= 7
def solve():
    result = -3 # Because of 1 and 2
    dFact = [1]
    for n in range(1, 10):
        dFact.append(dFact[-1] * n)
    for d0 in range(0, 10):
        n0 = d0
        sf0 = 0
        if n0 > 0:
            sf0 += dFact[d0]
        for d1 in range(0, 10):
            n1 = 10 * n0 + d1
            sf1 = sf0
            if n1 > 0:
                sf1 += dFact[d1]
            for d2 in range(0, 10):
                n2 = 10 * n1 + d2
                sf2 = sf1
                if n2 > 0:
                    sf2 += dFact[d2]
                for d3 in range(0, 10):
                    n3 = 10 * n2 + d3
                    sf3 = sf2
                    if n3 > 0:
                        sf3 += dFact[d3]
                    for d4 in range(0, 10):
                        n4 = 10 * n3 + d4
                        sf4 = sf3
                        if n4 > 0:
                            sf4 += dFact[d4]
                        for d5 in range(0, 10):
                            n5 = 10 * n4 + d5
                            sf5 = sf4
                            if n5 > 0:
                                sf5 += dFact[d5]
                            for d6 in range(0, 10):
                                n6 = 10 * n5 + d6
                                sf6 = sf5
                                if n6 > 0 and sf6 + dFact[d6] == n6:
                                    result += n6
    return result

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
