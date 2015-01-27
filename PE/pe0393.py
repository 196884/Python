def step(d, N):
    # pretty horific code to do simple stuff below... I should really learn how to use dictionaries in Python!
    result = dict()
    for pattern, patternCount in d.iteritems():
        prefixes = dict()
        prefixes[(0, 0)] = 1
        p3 = 1
        p = pattern
        for k in range(0, N):
            s = p % 3
            prefixesNew = dict()
            if s == 1: # There's one going down here...
                for (prefix, imbalance), prefixCount in prefixes.iteritems():
                    if imbalance == 0:
                        k1 = (prefix + p3, 0)
                        c1 = prefixesNew.get(k1, 0)
                        prefixesNew[k1] = c1 + prefixCount
                        k0 = (prefix, -1)
                        c0 = prefixesNew.get(k0, 0)
                        prefixesNew[k0] = c0 + prefixCount
                    elif imbalance == 1:
                        k0 = (prefix, 0)
                        c0 = prefixesNew.get(k0, 0)
                        prefixesNew[k0] = c0 + prefixCount
            elif s == 0:
                for (prefix, imbalance), prefixCount in prefixes.iteritems():
                    if imbalance == -1:
                        k1 = (prefix + p3, 0)
                        c1 = prefixesNew.get(k1, 0)
                        prefixesNew[k1] = c1 + prefixCount
                        k0 = (prefix, -1)
                        c0 = prefixesNew.get(k0, 0)
                        prefixesNew[k0] = c0 + prefixCount
                    elif imbalance == 0:
                        k1 = (prefix + p3, 1)
                        c1 = prefixesNew.get(k1, 0)
                        prefixesNew[k1] = c1 + prefixCount
                        k2 = (prefix + 2 * p3, -1)
                        c2 = prefixesNew.get(k2, 0)
                        prefixesNew[k2] = c2 + prefixCount
                    elif imbalance == 1:
                        k2 = (prefix + 2 * p3, 0)
                        c2 = prefixesNew.get(k2, 0)
                        prefixesNew[k2] = c2 + prefixCount
                        k0 = (prefix, 1)
                        c0 = prefixesNew.get(k0, 0)
                        prefixesNew[k0] = c0 + prefixCount
            else: # There's one going up here...
                for (prefix, imbalance), prefixCount in prefixes.iteritems():
                    if imbalance == -1:
                        k0 = (prefix, 0)
                        c0 = prefixesNew.get(k0, 0)
                        prefixesNew[k0] = c0 + prefixCount
                    elif imbalance == 0:
                        k2 = (prefix + 2 * p3, 0)
                        c2 = prefixesNew.get(k2, 0)
                        prefixesNew[k2] = c2 + prefixCount
                        k0 = (prefix, 1)
                        c0 = prefixesNew.get(k0, 0)
                        prefixesNew[k0] = c0 + prefixCount
            prefixes = prefixesNew
            p /= 3
            p3 *= 3
        for (prefix, imbalance), prefixCount in prefixes.iteritems():
            if 0 == imbalance:
                c = result.get(prefix, 0)
                result[prefix] = c + patternCount * prefixCount
    return result

def countSolutions(N):
    d = dict()
    d[0] = 1
    for k in range(0, N):
        d = step(d, N)
    return d.get(0, 0)

def solve():
    """
    In the encoding (base 3):
    1 goes down
    2 goes up
    """
    return countSolutions(10)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
