import math

def minN(p, q, t):
    d = math.sqrt(p) - math.sqrt(q)
    if d >= 1.0:
        return 0
    x = -t * math.log(10) / math.log(d) / 2
    return math.ceil(x)

def solve():
    # if rp = sqrt(p) and rq = sqrt(q), then:
    # (rp + rq) ^ 2k + (rp - rq) ^ 2k
    # is an integer.
    #
    # if (rp + rq) ^ 2k has exactly m '9's, then
    # (rp - rq) ^ 2k is in the range ]10^(-m-1), 10^(-m)], or
    # 2k log_10(rp - rq) is in the range ]-m-1, -m] or
    # -2k log_10(rp - rq) is in the range [m, m+1[
    r = 0
    for p in range(1, 2011):
        for q in range(1, p):
            if p + q <= 2011:
                r += minN(p, q, 2011)
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
