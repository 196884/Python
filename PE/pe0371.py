from decimal import *
getcontext().prec = 30

def solve():
    N = Decimal(1000)
    s = (Decimal(501)/Decimal(250), Decimal(2))
    k = 498
    while k >= 0:
        s1 = N / (N - Decimal(k+1)) + (N - Decimal(2*k+2)) * s[1] / (N - Decimal(k+1))
        s0 = (N+s1) / (N - Decimal(k+1)) + (N - Decimal(2*k+2)) * s[0] / (N - Decimal(k+1))
        s  = (s0, s1)
        k -= 1
    print s[0]
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
