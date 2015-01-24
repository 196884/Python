def powMod(a, b, m):
    a2k    = a # a^(2^k)
    result = 1
    while b > 0:
        if b % 2 == 1:
            result = (result * a2k) % m
        a2k = (a2k * a2k) % m
        b /= 2
    return result

def orderAux(m, k, d, p, pk, dk, pInfo):
    if 1 == p:
        return d
    a = powMod(10, k / pk, m)
    while 1 != a:
        d *= p
        a = powMod(a, p, m)
    dk *= pk
    (q, qk) = pInfo[k / dk]
    r = orderAux(m, k, d, q, qk, dk, pInfo)
    return r

def solve():
    # Naive, slow-ish, but good enough
    # It's actually overkill at this point to precompute phi,
    # since the solution is likely to be just above 10**6, so starting
    # there and computing phi 'naively' should be good enough
    B = 200000
    # pInfo[n] = (p, p^k) where:
    pInfo = [(1, 1) for i in range(0, B+1)]
    phi = [1 for i in range(0, B+1)]
    # * p is the largest prime factor of n
    # * p^k is the highest power of p dividing n
    r = 0
    f = 0
    for n in range(2, B+1):
        (p, pk) = pInfo[n]
        isPrime = False
        if 1 == p:
            isPrime = True
            p = n
            pk = p
            phi[n] = p - 1
            while pk <= B:
                mpk = pk
                while mpk <= B:
                    pInfo[mpk] = (p, pk)
                    mpk += pk
                pk *= p
        else:
            phi[n] = (pk / p) * (p - 1) * phi[n / pk]
        if n % 9 == 0 and n % 2 > 0 and n % 5 > 0:
            m = n / 9
            if phi[m] < m-1:
                # we must check that 10 is of the right order:
                (p, pk) = pInfo[phi[n]]
                k = orderAux(n, phi[n], 1, p, pk, 1, pInfo)
                m = n / 9
                if m > 1 and (m-1) % k == 0:
                    r += m
                    f += 1
                    if 25 == f:
                        return r
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
