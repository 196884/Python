# The goal is to return the largest prime factor of
# 600851475143

import array

def iterateState(s):
    r = dict()
    for k, n in s.iteritems():
        k0 = k % 11
        k1 = (k / 11) % 11
        k2 = (k / 121) % 11
        k3 = (k / 1331) % 11
        
        if k0 > 0:
            i1 = k0 - 1 + 11 * ( k1 + 1 + 11 * ( k2 + 11 * ( k3 ) ) )
            a = r.get(i1, 0)
            r[i1] = a + n * k0
        if k1 > 0:
            i2 = k0 + 11 * ( k1 - 1 + 11 * ( k2 + 1 + 11 * ( k3 ) ) )
            a = r.get(i2, 0)
            r[i2] = a + n * k1
        if k2 > 0:
            i3 = k0 + 11 * ( k1 + 11 * ( k2 - 1 + 11 * ( k3 + 1 ) ) )
            a = r.get(i3, 0)
            r[i3] = a + n * k2
    return r

def solve():
    s = dict()
    s[20] = 9
    for i in range(0, 17):
        s = iterateState(s)
    return sum(s.values())

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
