def T(n):
    # Returns the n-th triangular number
    return n * (n + 1) / 2

def f(n):
    # if n = a_0 + a_1.7 + a_2.7^2 +... + a_k.7^k,
    # successively computes the result for the partial sums up to 7^j
    j   = 0
    p7  = 1 # the current 7^j
    r   = 0 # the current partial decomposition
    t   = 0 # the result up to a_j.7^j
    f   = 0 # the result up to 7^j-1
    sub = 0
    while n > 0:
        aj  = n % 7
        tU  = T(aj) * f + T(aj-1) * sub
        tD  = (aj + 1) * t + aj * ((r+1) * (p7-1) - T(r))
        t   = tU + tD
        f   = T(7) * f + T(6) * sub
        r  += aj * p7
        p7 *= 7
        sub = T(p7-1) # the count of the largest triangular sub-motive
        n  /= 7
    return t

def solve():
    n = 10 ** 9
    return T(n) - f(n-1)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

