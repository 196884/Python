def gcd(a, b):
    if a == b:
        return a
    if a < b:
        return gcd(b, a)
    if b == 0:
        return a
    return gcd(b, a%b)

def solve():
    p = 1009
    q = 3643
    phi = (p-1) * (q-1)
    r = 0
    for e in range(2, phi):
        if gcd(e-1, p-1) == 2 and gcd(e-1, q-1) == 2 and gcd(e, phi) == 1:
            r += e
    return r
    
if __name__ == "__main__":
    result = solve()
    print "Result: %s" % result
