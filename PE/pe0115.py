def f(m, n):
    # direct dynamic programming solution
    l = [ 1 ] # only one way to obtain length 0
    nMax = n 
    for n in range(1, nMax+1):
        r = l[-1] # case where a black block is added
        i = m
        while i < n:
            # one block of size i, n-i to be filled
            r += l[n-i-1]
            i += 1
        if n >= m:
            r += 1
        l.append(r)
    return l[-1]

def solve():
    n = 0
    while f(50, n) < 1000000:
        n += 1
    return n

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

