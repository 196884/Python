from mpmath import mp

mp.dps = 30

# Descartes theorem gives:
def getRadius(r1, r2, r3):
    k1 = 1/r1
    k2 = 1/r2
    k3 = 1/r3
    k4 = k1 + k2 + k3 + 2 * mp.sqrt(k1*k2 + k2*k3 + k3*k1)
    return 1/k4

def rec(depth, r1, r2, r3):
    if depth == 0:
        return 0
    r4 = getRadius(r1, r2, r3)
    r = r4 ** 2 + rec(depth-1, r1, r2, r4) + rec(depth-1, r2, r3, r4) + rec(depth-1, r3, r1, r4)
    return r
    
def solve():
    r0 = 2*mp.sqrt(3.0)-3
    n = 10
    r = 1 - 3 * r0 ** 2 - 3 * rec(n, r0, r0, -1) - rec(n, r0, r0, r0)
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %s" % str(result)
