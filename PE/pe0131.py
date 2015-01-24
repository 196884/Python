def checkCube(n, s = 1):
    # s is the start point
    e = s
    e3 = s * s * s
    while e3 <= n:
        e3 *= 8
        e *= 2
    s3 = e3 / 8
    s = e / 2
    # at this point, n \in [s3, e3[
    while e - s > 1:
        m = (s + e) / 2
        m3 = m * m * m
        if n >= m3:
            s = m
        else:
            e = m
    return n == s * s * s

def check(p):
    a = 1
    while p >= 3 * a * (a + 1) + 1:
        if checkCube(p + a * a * a, a):
            return True
        a += 1
    return False

def solve():
    """
    a^3 + p.a^2 = b^3
    so a^2 divides b^3
    p cannot divide a (otherwise, we would get an equation of the form a^2 (a + 1) = b^3...)
    so a and p are coprime, and:
    a^2 (a + p) = b^3
    so both a^2 and a+p must be cubes, and in fact a must be a cube
    """
    B = 10 ** 6
    isPrime = [True for n in range(0, B+1)]
    r = 0
    for n in range(2, B+1):
        if isPrime[n]:
            p = n
            if check(p):
                print "Found %d" % p
                r += 1
            pk = 2 * p
            while pk <= B:
                isPrime[pk] = False
                pk += p
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
