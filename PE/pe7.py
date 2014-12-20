import pe3 as pe3

def solve():
    n = 100000
    l = pe3.primeSieve(n)
    while len(l) < 10000:
        n *= 2
        l = pe3.primeSieve(n)
    return l[10000]

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

