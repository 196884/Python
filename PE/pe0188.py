def powMod(a, b, m):
    a2k    = a # a^(2^k)
    result = 1
    while b > 0:
        if b % 2 == 1:
            result = (result * a2k) % m
        a2k = (a2k * a2k) % m
        b /= 2
    return result

def phi(k2, k5):
    if k2 == 0:
        return (0, 0)
    if k5 == 0:
        return (k2-1, 0)
    return (k2+1, k5-1)

def aux(x, y, k2, k5):
    # returns x ^^ y mod 2^k2.^k5
    if 1 == k2 and 0 == k5:
        return 1
    (k2b, k5b) = phi(k2, k5)
    yAux = aux(x, y-1, k2b, k5b)
    m = 2 ** k2 * 5 ** k5
    r = powMod(x, yAux, m)
    return r

def solve():
    return aux(1777, 1855, 8, 8)
 
if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
