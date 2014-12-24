def f(n):
    # direct dynamic programming solution
    # m is the unit tile length, n the length to be replaced
    l = [ 1 ]
    nMax = n 
    for n in range(1, nMax+1):
        r = l[-1] # case where a black block is added
        if n >= 2:
            r += l[n-2]
        if n >= 3:
            r += l[n-3]
        if n >= 4:
            r += l[n-4]
        l.append(r)
    return l[-1]

def solve():
    return f(50)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

