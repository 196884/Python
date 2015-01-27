def solve():
    # We use Wilson's theorem
    B = 10**8
    B2 = B / 2
    # isPrime[i] is True iff 2*i+1 is prime
    isPrime = [True for i in range(0, B2)]
    r = 0
    for n in range(1, B2):
        if isPrime[n]:
            p = 2 * n + 1
            pk = n + p
            while pk < B2:
                isPrime[pk] = False
                pk += p
            if n > 1: # we need to skip 3
                inv2 = (p + 1) / 2
                if p % 3 == 1:
                    inv3 = (p - 1) ** 2 / 3
                    inv3 = inv3 % p
                else:
                    inv3 = (p + 1) / 3
                x = inv2 * (inv3 - 1 - inv3 * inv2 ** 2)
                x = x % p
                r += x
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
