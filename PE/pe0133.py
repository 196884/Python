def powMod(a, b, m):
    a2k    = a # a^(2^k)
    result = 1
    while b > 0:
        if b % 2 == 1:
            result = (result * a2k) % m
        a2k = (a2k * a2k) % m
        b /= 2
    return result

def check(p):
    l = powMod(10, 10, p)
    h = powMod(10, 100, p)
    while 1 != l and l != h:
        l = powMod(l, 10, p)
        h = powMod(h, 100, p)
    return 1 == l


def solve():
    # To go faster: the order of 10 mod p divides phi(p) = p-1,
    # so we should check the gcd of p-1 with 10**9...
    B = 100000
    isPrime = [True for n in range(0, B+1)]
    r = 5
    for n in range(2, B+1):
        if isPrime[n]:
            p = n
            pk = 2 * p
            while pk <= B:
                isPrime[pk] = False
                pk += p
            if p > 3 and not check(p):
                r += p
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
