def solve():
    # We only count the increasing ones, as there should be as many decreasing.
    # Using dynamic programming, and removing the 9
    n = 100
    increasing = [ 1 for i in range(0, 10) ]
    decreasing = [ 1 for i in range(0, 10) ]
    sumDec     = 9
    k = 1
    # l[i] is the number of k-digit increasing numbers starting with a 'i'
    while k < n:
        k += 1
        incNew = []
        decNew = []
        for i in range(0, 10):
            incNew.append(sum([increasing[j] for j in range(i, 10)]))
            decNew.append(sum([decreasing[j] for j in range(0, i+1)]))
        increasing = incNew
        decreasing = decNew
        # the decreasing which first (non-zero) digit is the k-th (from the right)
        sumDec    += sum([decreasing[j] for j in range(1, 10)])
    # sumDec is up to date, except it doesn't count zero:
    sumDec += 1
    sumInc  = sum(increasing)
    # the intersection of increasing and decreasing needs to be removed:
    # the '2' is for zero
    result  = sumInc + sumDec - 9 * n - 2
    return result

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
