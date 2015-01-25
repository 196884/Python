def check(l, primes):
    n = 1
    pn = 1
    for i, k in enumerate(l):
        p = primes[i]
        n *= p ** k
        pn *= ( p - 1 ) * p ** ( k - 1 )
    if 94744 * pn < 15499 * ( n - 1 ):
        return n
    return 0

def solve():
    # Close to pe0110, handled the same way...
    primes = [ 2, 3, 5, 7, 11, 13, 17, 19, 23 ]
    l = [3, 1, 1, 1, 1, 1, 1, 1, 1]
    return check(l, primes)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
