import array

def solve():
    N = 10**8
    phi = array.array('i', (0 for i in range(0, N+1)))
    ps = array.array('i', (1 for i in range(0, N+1)))
    pks = array.array('i', (1 for i in range(0, N+1)))
    phi[1] = 1
    phi[ 1 ] = 1
    r = 0
    for n in range(2, N+1):
        p = ps[n]
        if 1 == p:
            p = n
            pk = p
            phi[n] = p - 1
            while pk <= N:
                mpk = pk
                while mpk <= N:
                    ps[mpk] = p
                    pks[mpk] = pk
                    mpk += pk
                pk *= p
        else:
            phi[n] = (pks[n] / p) * (p - 1) * phi[n / pks[n]]
    r = 1 + 3 * N * (N + 1) - 7 - 6 * (sum(phi) - 1)
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
