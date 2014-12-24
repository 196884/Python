def f(m, n):
    # direct dynamic programming solution
    # m is the unit tile length, n the length to be replaced
    l = [ 1 ]
    nMax = n 
    for n in range(1, nMax+1):
        r = l[-1] # case where a black block is added
        if n >= m:
            r += l[n-m]
        l.append(r)
    return l[-1]-1 # there must be at least one, so we remove the 'all black' case

def solve():
    return f(2, 50) + f(3, 50) + f(4, 50)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

