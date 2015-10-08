def solve():
    r = 0
    for x0 in range(0, 10):
        for x5 in range(0, 10):
            for x10 in range(0, 10):
                for x15 in range(0, 10):
                    s = x0 + x5 + x10 + x15
                    x6Max = min(10, s+1)
                    x6Min = max(0, s-27)
                    for x6 in range(x6Min, x6Max):
                        s6 = s-x6
                        x9Max = min(10, s6+1)
                        x9Min = max(0, s6-18)
                        for x9 in range(x9Min, x9Max):
                            s9 = s6 - x9
                            x12Max = min(10, s9+1)
                            x12Min = max(0, s9-9)
                            for x12 in range(x12Min, x12Max):
                                x3 = s9-x12
                                if x3 >= 0 and x3 < 10:
                                    s59 = s - x5 - x9
                                    x1Max = min(10, s59+1)
                                    x1Min = max(0, s59-9)
                                    for x1 in range(x1Min, x1Max):
                                        x13 = s59 - x1
                                        x2 = s - x0 - x1 - x3
                                        x14 = s - x2 - x6 - x10
                                        s261014 = x2 + x6 + x10 + x14
                                        if x13 >= 0 and x13 < 10 and x2 >= 0 and x2 < 10 and x14 >= 0 and x14 < 10 and s261014 == s:
                                            s56 = s - x5 - x6
                                            x4Max = min(10, s56+1)
                                            x4Min = max(0, s56-9)
                                            for x4 in range(x4Min, x4Max):
                                                x7 = s56 - x4
                                                x8 = s - x0 - x4 - x12
                                                x11 = s - x3 - x7 - x15
                                                s891011 = x8 + x9 + x10 + x11
                                                if x7 >= 0 and x7 < 10 and x8 >= 0 and x8 < 10 and x11 >= 0 and x11 < 10 and s891011 == s:
                                                    r += 1
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
