from mpmath import *
import itertools as itt

mp.dps = 30

def h(d, a, b):
    h2 = d * (2 * (a + b) - d)
    return h2 ** mpf(0.5)

def totalHeight(d, l):
    acc = l[0] + l[-1]
    for i in range(1, len(l)):
        acc += h(d, l[i-1], l[i])
    return acc

def solve():
    d = mpf(100000.0)
    rMin = 30
    rMax = 50
    l = []
    r = rMax
    while r >= rMin:
        l.append(mpf(r * 1000))
        r -= 2
    r = rMin + 1
    while r <= rMax:
        l.append(mpf(r * 1000))
        r += 2
    return int(totalHeight(d, l))
 
if __name__ == "__main__":
    result = solve()
    print "Result: %s" % result
