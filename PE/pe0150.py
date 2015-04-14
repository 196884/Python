def rowStart(h, B):
    k = (B - 1 - h)
    return k * (k + 1) / 2

def rowLength(h, B):
    return B - h

def buildT(B):
    T = []
    t = 0
    m1 = 2 ** 19
    m2 = 2 * m1
    M = B * (B + 1) / 2
    for k in range(0, M):
        t = ( 615949 * t + 797807 ) % m2
        T.append( t - m1 )
    return T

def solve():
    # Pretty bruteforce, but works
    #B = 6
    #T = [15, -14, -7, 20, -13, -5, -3, 8, 23, -26, 1, -4, -5, -18, 5, -16, 31, 2, 9, 28, 3]
    B = 1000
    T = buildT( B )
    result = 0
    p2 = []
    r0 = rowStart(0, B)
    rl = rowLength(0, B)
    for i in range(0, rl):
        x = T[ r0 + i ]
        p2.append( x )
        result = min(result, x)

    p1 = []
    r0 = rowStart(1, B)
    rl = rowLength(1, B)
    for i in range(0, rl):
        x = T[ r0 + i ]
        p1.append( x )
        result = min(result, x)
        y = x + p2[i] + p2[i+1]
        p1.append( y )
        result = min(result, y)

    for h in range(2, B-1):
        p = []
        r0 = rowStart(h, B)
        rl = rowLength(h, B)
        for i in range(0, rl):
            x = T[ r0 + i ]
            p.append( x )
            result = min(result, x)
            y = x + p1[ h * i ] + p1[ h * (i + 1) ]
            p.append( y )
            result = min(result, y)
            for j in range(1, h):
                z = x + p1[ h * i + j ] + p1[ h * (i + 1) + j ] - p2[ (h - 1) * (i + 1) + j - 1 ]
                p.append( z )
                result = min(result, z)
        p2 = p1
        p1 = p
        print "Done with h=%d" % h

    return result
           
if __name__ == "__main__":
    result = solve()
    print "Result: %s" % str(result)
