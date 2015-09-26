from mpmath import *

mp.dps = 30

def maxVal(k):
    a = mpf(2)/mpf(k+1)
    r = mpf(1)
    for i in range(1, k+1):
        r *= (mpf(i) * a) ** i
    return floor(r)

def solve():
    r = 0
    for k in range(2, 16):
        r += maxVal(k)
    return r
  
if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
