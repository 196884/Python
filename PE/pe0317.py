import math

def solve():
    # Basically worked out a closed form:
    y0 = 100.0
    v = 20.0
    g = 9.81
    pi = 4. * math.atan(1.)
    a = v * v / g
    r = pi * a * (y0 + a / 2) ** 2
    print r
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
