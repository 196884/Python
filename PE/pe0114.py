def solve():
    # direct dynamic programming solution
    l = [ 1 ] # only one way to obtain length 0
    nMax = 50 
    for n in range(1, nMax+1):
        r = l[-1] # case where a black block is added
        i = 3
        while i < n:
            # one block of size i, n-i to be filled
            r += l[n-i-1]
            i += 1
        if n >= 3:
            r += 1
        l.append(r)
    return l[-1]

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

