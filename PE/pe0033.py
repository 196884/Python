def gcd(a, b):
    if b > a:
        return gcd(b, a)
    if b == 0:
        return a
    return gcd(b, a%b)

def solve():
    accN = 1
    accD = 1
    for n1 in range(1, 10):
        for n0 in range(1,10):
            n = 10 * n1 + n0
            for d1 in range(1, 10):
                for d0 in range(1, 10):
                    d = 10 * d1 + d0
                    if ( n1 != d1 or n0 != d0 ) and n < d and (n1 == d0 or n0 == d1) and ( n1*d == n*d0 or n0*d == n*d1):
                        accN *= n
                        accD *= d
    g = gcd(accN, accD)
    return accD / g

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
