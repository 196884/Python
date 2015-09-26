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
    N = 10**12
    r = set([1])
    k = 2
    kMax = iSqrt(N)
    for k in range(2, kMax+1):
        # Handling base k:
        kp = k * k
        acc = 1 + k + kp
        while acc <= N:
            r.add(acc)
            kp *= k
            acc += kp
    return sum(r)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
