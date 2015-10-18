def computeP(n):
    r = [[1 for i in range(n+1)] for j in range(n+1)]
    for s in range(2 * n + 1):
        for i in range(1, s):
            if i <= n and s-i <= n:
                r[i][s-i] = r[i-1][s-i] + r[i][s-i-1]
    return r

def getT(a, b, p):
    if a == 0 or b == 0:
        return None
    return p[a-1][b-1]

def computeU(n, p):
    r = [[None for i in range(n+1)] for j in range(n+1)]
    for a in range(1, n+1):
        for b in range(1, n+1):
            aux = 0
            for k in range(1, n):
                aux += getT(a, k, p) * getT(b, n-k, p)
            r[a][b] = aux
    return r
           
def solve():
    # We decompose as follows:
    # * p[a][b] is the # ways to (legally) tile 2 parallel segments of lengths a and b
    # * u[a][b] is the # ways to (legally) tile a 'U' shape, with two opposite parallel 
    #   segments of lengths a and b, and the segment connecting them to finish the U of length n
    # * getT(a, b) is the # ways to (legally) tile a corner triangle with two adajacent segments
    #   of lengths a and b
    # * 2 * D is the number of tilings of the whole square that contain one diagonal
    # * 4 * C1 is the number of tilings where a single corner is connected to a single other side
    # * 2 * C3 is the number of tilings where two corners on the same side are both connected to the opposite side
    # * 2 * C2 is the number of tilings where two opposite corners are connected to two opposite sides, excepted
    #   those that contain a diagonal
    # * 4 * C is the number of corners where a corner is connected to the two opposite sides (excepted those that
    #   contain a diagonal)
    # * S is the number of tilings where one side is connected to the other (not counting connections starting at corners)
    n = 30
    p = computeP(n)
    u = computeU(n, p)
    # D: diagonal taken
    D  = getT(n, n, p) ** 2
    C1 = 0
    for a1 in range(1, n):
        for b in range(1, n):
            for a2 in range(a1, n):
                C1 += getT(n-1, a1, p) * p[b][a2-a1] * u[n-a2][n-b]
    C2 = 0
    for a1 in range(1, n):
        for a2 in range(a1, n):
            C2 += getT(n-1, a1, p) * getT(n-1, n-a2, p) * p[n][a2-a1]
    C3 = 0
    for a1 in range(1, n):
        for b1 in range(1, n):
            # The -1 is to remove the unique one having the diagonal
            C3 += getT(n-1, a1, p) * getT(n-1, n-b1, p) * ( p[n-a1][b1] - 1 )
    # C: from one corner to each of the other 2 sides
    C = 0
    for a in range(1, n):
        for b in range(1, n):
            C += getT(n, n-a, p) * getT(n, n-b, p) * getT(a, b, p)
    # S: single side only
    S = 4 * C1 + 2 * C2 + 2 * C3
    for a1 in range(1, n):
        for b1 in range(1, n):
            for a2 in range(a1, n):
                for b2 in range(b1, n):
                    S += u[a1][b1] * u[n-a2][n-b2] * p[a2-a1][b2-b1]
    r = 2 * D + 4 * C + 2 * S
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
