def gcd(a, b):
    if b > a:
        return gcd(b, a)
    if b == 0:
        return a
    return gcd(b, a%b)

def solve():
    # We use the parametrization of Pythagorean triplets:
    LMax = 1500000
    r = [0 for i in range(0, LMax + 1)]
    m = 1
    m2 = m * m
    while 2 * m2 <= LMax:
        for n in range(1, m):
            if (m+n) % 2 == 1 and gcd(m, n) == 1:
                l = 2 * m * ( m + n )
                lk = l
                k = 1
                while lk <= LMax:
                    a = k * ( m2 - n * n )
                    b = k * 2 * m * n
                    c = k * ( m2 + n * n )
                    r[lk] += 1
                    lk += l
                    k += 1
        m += 1
        m2 = m * m
    l = [1 for i in range(0, LMax + 1) if r[i] == 1]
    return sum(l)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
