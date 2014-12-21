def invCycleLength(n):
    # remToIndex is the mapping from remainders to when they were first seen
    rem = 1
    remToIndex = {1: 0}
    index = 0
    while True:
        rem *= 10
        q = rem / n
        rem = rem - q * n
        if 0 == rem:
            return 0
        prevIdx = remToIndex.get(rem, -1)
        index += 1
        if prevIdx >= 0:
            return index - prevIdx
        remToIndex[rem] = index


def solve():
    result = 0
    value = 0
    for n in range(1, 1000):
        v = invCycleLength(n)
        if v > value:
            result = n
            value = v
    return result

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
