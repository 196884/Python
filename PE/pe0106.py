import itertools as it

def solve():
    n = 12 
    r = 0
    values = range(0, n)
    # We generate all disjoint pairs of subsets of the same size:
    for subsetSize in range(1, n/2+1):
        subsets = it.combinations(values, subsetSize)
        for ss1, ss2 in it.combinations(subsets, 2):
            if( len(set(ss1).intersection(set(ss2))) == 0 ):
                # at this point, ss1 and ss2 are 2 disjoint subsets of the same length
                mult = 1
                if ss1[0] > ss2[0]:
                    mult = -1
                needsTest = False
                k = 1
                while k < subsetSize and not needsTest:
                    needsTest = (mult * ss1[k]) > (mult * ss2[k])
                    k += 1
                if needsTest:
                    r += 1
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
