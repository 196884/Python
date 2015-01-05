def iSqrt(n):
    """
    Integral square root (by Newton iterations)
    """
    x    = 1
    xOld = 1
    while True:
        aux = ( x + ( n / x ) ) / 2
        if aux == x:
            return x
        if aux == xOld:
            return min(x, xOld)
        xOld = x
        x = aux

def solve():
    # The most naive of solutions
    # Far too slow indeed (though I did manage to get the result!)
    # 
    # A much better idea is to use the parametrization of Pythagorean
    # triples to generate all such tuples (with a bound, function of M),
    # and for each such triple A<=B<=C, count how many valid configurations
    # a<=b<=c<=M are such that:
    # a+b = A and c = B
    # *or*
    # a+b = B and c = A
    #
    # My code for the above was bugged, so I ended up taking the shorter
    # path below
    nbFound = 0
    bound = 1000000
    M = 1
    while nbFound < bound:
        M2 = M ** 2
        for b in range(1, M+1):
            for a in range(1, b+1):
                s = (a+b) ** 2 + M2
                t = iSqrt(s)
                if t * t == s:
                    nbFound += 1
        M += 1
    return M-1

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
