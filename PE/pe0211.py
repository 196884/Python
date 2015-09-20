import array

def iSqrt(n):
    # Integral square root (by Newton iterations)
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
    n = 64000000
    sig2 = [ 0, 1 ]
    r = 1
    l = []
    for i in range(0, n):
        l.append((1, 1))
    for k in range(2, n):
        if k % 1000 == 0:
            print k
        (q, qpow) = l[k]
        if q == 1:
            # k is prime
            p = k
            ppow = p
            while ppow < n:
                ppowMul = ppow
                while ppowMul < n:
                    l[ppowMul] = (p, ppow)
                    ppowMul += ppow
                ppow *= p
            sig2.append(1+p*p)
            # cannot fit, since sigma_2(p) = 1 + p^2 cannot be a perfect square
        else:
            # k is not prime
            s2 = sig2[k / qpow] * (qpow * qpow * q * q - 1) / (q * q - 1)
            sig2.append(s2)
            r2 = iSqrt(s2)
            if r2 * r2 == s2:
                r += k
    return r

if __name__ == "__main__":
    result = solve()
    print "result: %s" % result
