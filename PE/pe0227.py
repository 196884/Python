from decimal import *
from fractions import Fraction

getcontext().prec = 60

def solve():
    f50 = (Fraction(2, 1), Fraction(8, 9), Fraction(1, 9))
    a = Fraction( 9 * 17 - 64, 9 )
    f49 = (52 / a, Fraction(80, 9) / a, 1 / a)
    l = [f50, f49]
    for k in reversed(range(2, 49)):
        rpp = l[-2]
        rp = l[-1]
        r2 = 1 / (Fraction(18, 1) - rpp[2] - rp[1] * (rpp[1] + Fraction(8, 1)))
        r0 = (Fraction(36, 1) + rpp[0] + rp[0] * (rpp[1] + Fraction(8, 1))) * r2
        r1 = (Fraction(8, 1) + rp[2] * (rpp[1] + Fraction(8, 1))) * r2
        l.append((r0, r1, r2))
    r2 = l[-1]
    r3 = l[-2]
    f1 = (Fraction(36, 1) + r3[0] + r2[0] * (r3[1] + Fraction(8, 1))) / (Fraction(17, 1) - r2[1] * (r3[1] + Fraction(8, 1)) - r3[2])
    f = [Fraction(0, 1), f1]
    li = list(reversed(l))
    for (a, b, c) in li:
        aux = a + b * f[-1] + c * f[-2]
        f.append(aux)
    x = f[-1]
    r = Decimal(x.numerator) / Decimal(x.denominator)
    print r
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
