def initList():
    r = []
    for i in range(0, 10):
        r.append([0 for j in range(0, 10)])
    return r

def solve():
    # dynamic programming:
    # after n steps, l[i][j] is the number of paths:
    # * of length n
    # * starting at 0
    # * going up or down by 1 at each step
    # * with minimum -i, and maximum +j
    r = 0
    l = initList()
    l[0][0] = 1
    for n in range(1, 40):
        lNew = initList()
        for i in range(0, 10):
            for j in range(0, 9):
                lNew[max(0, i-1)][j+1] += l[i][j]
                lNew[j+1][max(0, i-1)] += l[j][i]
        l = lNew
        for i in range(1, 10): # The starting with a 0 is covered in the previous count!
            r += l[i][9-i]

    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
