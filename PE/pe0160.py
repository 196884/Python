def powMod(a, b, m):
    a2k    = a # a^(2^k)
    result = 1
    while b > 0:
        if b % 2 == 1:
            result = (result * a2k) % m
        a2k = (a2k * a2k) % m
        b /= 2
    return result

def auxBase(b, m):
    # contribution of all numbers <=b, not divisible by 2 or 5:
    a = 1 
    l = [1]
    for n in range(1, m+1):
        if (n % 2 != 0) and (n % 5 != 0):
            a = (a * n) % m
        l.append(a)
        if n == b:
            return a
    q = b / m
    r = b % m
    a = (powMod(a, q, m) * l[r]) % m
    return a

def aux5(b, m):
    if b == 0:
        return 1
    else:
        return (aux5(b/5, m) * auxBase(b, m)) % m

def aux2(b, m):
    n = b
    r = 1
    while n > 0:
        r = (r * aux5(n, m)) % m
        n = n / 2
    return r

def solve():
    B = 10 ** 12
    # We do it in 3 parts:
    # * the numbers that are not divisible by 2 or 5
    # * the numbers that are divisible by 2 but not by 5
    # * the numbers that are divisible by 5
    #
    # Finally we add back the contribution of all the powers of 2
    M = 10 ** 5
    r = aux2(B, M)
    p5 = 5
    k5 = 0
    while p5 <= B:
        k5 += B / p5
        p5 *= 5

    p2 = 2
    k2 = 0
    while p2 <= B:
        k2 += B / p2
        p2 *= 2

    r = (r * powMod(2, k2 - k5, M)) % M
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
