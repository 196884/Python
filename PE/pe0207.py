from fractions import Fraction

def fn(p, q):
    return Fraction(p-1, 2**p - 1 - q)

def solve():
    # With the notations, there is such a partition iff
    # t = log_2(m) for some integer m >= 2
    # so P only changes values at integers of the form m^2 - m
    # 
    # the partition is perfect if m=2^p, and at such points, P has value
    # p / (2^p-1)
    # its value just before is (p-1)/(2^p-2)
    # We look for the first value of p such that (p-1)/(2^p-2) < 1/12345,
    # and then we look back to find the largest q such that:
    # (p-1)/(2^p-2-q) < 1/12345 (giving m = 2^p-1-q, and the answer should be m^2-m)
    threshold = Fraction(1, 12345)
    p = 2
    while fn(p, 1) >= threshold:
        p += 1
    # We now do a dichotomy between q = 1 and q = 2^(p-1)-1
    qMin = 1
    qMax = 2**(p-1)-1
    while qMax - qMin > 1:
        qMid = (qMin + qMax) / 2
        if fn(p, qMid) < threshold:
            qMin = qMid
        else:
            qMax = qMid
    m = 2**p - qMin
    return m ** 2 - m

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
