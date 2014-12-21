import pe3 as pe3

def solve():
    n = 20
    l = pe3.primeSieve(n)
    r = 1
    for p in l:
        pp = p
        aux = pp * p
        while aux <= n:
            pp = aux
            aux = pp * p
        r *= pp
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
