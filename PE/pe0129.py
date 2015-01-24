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
    B = 40000000
    # pInfo[n] = (p, p^k) where:
    pInfo = [(1, 1) for i in range(0, B+1)]
    phi = [1 for i in range(0, B+1)]
    # * p is the largest prime factor of n
    # * p^k is the highest power of p dividing n
    r = 0
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
        #print "n: %d, phi: %d" % (n, phi[n])
        B2 = 10 ** 6
        if phi[n] >= B2 and n % 9 == 0 and n % 2 > 0 and n % 5 > 0:
            # we must check that 10 is of the right order:
            (p, pk) = pInfo[phi[n]]
            k = orderAux(n, phi[n], 1, p, pk, 1, pInfo)
            if k >= B2:
                return n / 9
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result