def powMod(a, b, m):
    a2k    = a # a^(2^k)
    result = 1
    while b > 0:
        if b % 2 == 1:
            result = (result * a2k) % m
        a2k = (a2k * a2k) % m
        b /= 2
    return result


def solve():
    B = 1000000
    isPrime = [True for n in range(0, B+1)]
    r = 0
    k = 0
    for n in range(2, B+1):
        if isPrime[n]:
            p = n
            pk = 2 * p
            while pk <= B:
                isPrime[pk] = False
                pk += p
            if p > 3:
                if 1 == powMod(10, 10 ** 9, p):
                    r += p
                    k += 1
                    if k == 40:
                        return r
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
