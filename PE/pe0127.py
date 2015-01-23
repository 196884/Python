def gcd(a, b):
    if a == b:
        return a
    if a < b:
        return gcd(b, a)
    if b == 0:
        return a
    return gcd(b, a%b)

def solve():
    B = 120000
    pInfo = [(1, 1) for i in range(0, B+1)]
    primes = []
    rad = [0, 1]
    for n in range(2, B+1):
        (p, pk) = pInfo[n]
        if 1 == p:
            # n is prime
            p = n
            primes.append(p)
            pk = p
            while pk <= B:
                pkm = pk
                while pkm <= B:
                    pInfo[pkm] = (p, pk)
                    pkm += pk
                pk *= p
        (p, pk) = pInfo[n]
        rad.append(p * rad[n / pk])
    c_radc = []
    for c in range(1, B):
        c_radc.append((c, rad[c], c/rad[c]))
    c_radc.sort(key = lambda c: -c[2])

    r = 0
    for b in range(2, B):
        rb = rad[b]
        i  = 0
        while c_radc[i][2] > rb:
            c = c_radc[i][0]
            rc = rad[c]
            if c > b and c - b < b and gcd(c, b) == 1:
                a = c - b
                if rad[a] * rb * rc < c:
                    r += c
            i += 1
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
