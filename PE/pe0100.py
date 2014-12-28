def matMult(l1, l2):
    r = [[l1[0][0]*l2[0][0] + l1[0][1]*l2[1][0], l1[0][0]*l2[0][1]+l1[0][1]*l2[1][1]],
         [l1[1][0]*l2[0][0] + l1[1][1]*l2[1][0], l1[1][0]*l2[0][1]+l1[1][1]*l2[1][1]]]
    return r

def check(l, b):
    return (l[0][0]+1) / 2 >= b

def matPow(l, k):
    r = [[1, 0], [0, 1]]
    l2n = list(l)
    while k > 0:
        if k % 2 == 1:
            r = matMult(r, l2n)
        l2n = matMult(l2n, l2n)
        k /= 2
    return r

def solve():
    # We're looking for a and b such that:
    # a(a-1) / (c(c-1)) = 1/2
    # i.e.
    # (2c-1)^2-2(2a-1)^2 = 1
    # so we're solving a Pell equation.
    # Since y = 1, x = 1 is the minimal solution,
    # the set of solutions is given by
    # M^(2k+1) (1, 0)
    # where
    # M = ( 1  2 )
    #     ( 1  1 )

    b = 10 ** 12
    l = [[1, 2], [1, 1]]
    kD = 1
    lD = l
    kU = 1
    lU = l
    while not check(lU, b):
        lU = matMult(lU, lU)
        kU *= 2
    while kU - kD > 1:
        kM = (kD + kU) / 2
        lM = matPow(l, kM)
        if check(lM, b):
            kU = kM
            lU = lM
        else:
            kD = kM
            lD = lM
    if kU % 2 == 0:
        kU += 1
        lU = matMult(lU, l)
    return (lU[1][0] + 1) / 2

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
