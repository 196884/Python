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

def isSqr(n):
    if n <= 0:
        return False
    r = iSqrt(n)
    result = r * r == n
    return result

# We use the fact that all the angles are equal at the Torricelli point,
# so that p^2+q^2+pq = c^2 (...),
# so we use a technique similar to Pythagorean triple generation to generate
# such triples:
def solve():
    B = 120000
    rB = iSqrt(B)
    sols = set()
    squares = [ set() for i in range(0, B+1) ]
    for m in range(1, 1000):
        for n in range(1, m):
            p = 2 * m * n + n * n
            q = m * m - n * n
            k = 1
            while ( k * p <= B ) and ( k * q <= B ):
                squares[ k * p ].add( k * q )
                squares[ k * q ].add( k * p )
                k += 1
    for p in range(1, B+1):
        sp = squares[ p ]
        for q in sp:
            sq = squares[ q ]
            for r in sq:
                s = p+q+r
                if ( s <= B ) and ( p in squares[ r ] ):
                    sols.add( s )
    result = 0
    for s in sols:
        result += s
    return result

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
