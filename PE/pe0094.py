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
    # We're looking for a triangle with sides a, a and a+e (e=+/-1)
    # We let b be the height the divides it into 2 symmetric right triangles,
    # we must have:
    #     4b^2 + (a+2)^2 = 4a^2
    # 
    # b is either an integer or a half-integer. However, we also want to have
    # an integral area, which then implies that 2 must divide a+e, but then
    # the equation above implies that b must be an integer (reduce mod 4).
    # 
    # If we let a = 2x+e, then the equation becomes:
    #     (3x+e)^2 - 3b^2 = 1
    # 
    # Again, this is a Pell equation, which we solve as:
    # M = ( 2  3 )
    #     ( 1  2 )
    # 
    # If M^n = ( pn  ... )
    #          ( qn  ... )
    # 
    # then this parametrizes solutions with
    #   3x+e = pn
    #   b    = qn
    # 
    # (One easily proves that for all n, pn is not 0 mod 3)
    # 
    # Since the perimeter is 3a+e = 6x+4e = 2(pn+e), and M^1 corresponds
    # to a degenerate triangle, if we let nMax be the maximal n such that
    # 2(pn+e) <= 10 ** 9, then the result should be nMax - 1
    lMax = 10 ** 9
    l = [[2, 3], [1, 2]]
    r = 0
    lk = matMult(l, l)
    pn = lk[0][0]
    e = 1
    if pn % 3 == 2:
        e = -1
    else:
        e = 1
    while 2 * (pn + e) <= lMax:
        r += 2 * (pn + e)
        lk = matMult(lk, l)
        pn = lk[0][0]
        if pn % 3 == 2:
            e = -1
        else:
            e = 1
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
