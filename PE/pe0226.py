from mpmath import *

mp.dps = 30

def intersection():
    pL = (mpf(0), mpf(0))
    pU = (mpf(0.5), mpf(0.5))
    while pU[0] - pL[0] > mpf(0.1) ** 20:
        xM = (pL[0] + pU[0]) / 2.0
        yM = (pL[1] + pU[1]) / 2.0 + xM - pL[0]
        # we check whether (xM, yM) is within the circle:
        if (xM - mpf(0.25)) ** 2 + (yM - mpf(0.5)) ** 2 < mpf(0.25) **2:
            pU = (xM, yM)
        else:
            pL = (xM, yM)
    return (xM, yM)

def integral(x):
    i = mpf(0)
    b = mpf(0.5)
    pi = mpf(-1)
    while i - pi > mpf(0.1) ** 20:
        n = int(x / b)
        pi = i
        i += n * mpf(0.5) * b * b
        rx = x - n * b
        if n % 2 == 0:
            i += rx * rx * mpf(0.5)
        else:
            i += rx * (b - mpf(0.5) * rx)
        b = b * mpf(0.5)
    return i
          
def solve():
    # We first get the (non-trivial) intersection point of the curve
    # with the circle, call it (a, b):
    r = mpf(0.25)
    (x, y) = intersection()
    ix = integral(x)
    t = mpf(0.25) - ix - mpf(0.125) + pi * r * r * mpf(0.25) - y * (mpf(0.25) - x)
    dh = y - mpf(0.25)
    rca = mpf(0.5) - y
    rsa = mpf(0.25) - x
    a = acos(rca/r)
    ca = mpf(1.0) - dh / r
    t += mpf(0.5) * ( r * r * a - rca * rsa )
    return str(t)
 
if __name__ == "__main__":
    result = solve()
    print "Result: %s" % result
