def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        (g, y, x) = egcd(b % a, a)
        return (g, x - (b / a) * y, y)

def modInv(a, p):
    (g, x, y) = egcd(a, p)
    return x % p

def modPow(a, k, p):
    bits = []
    while k > 0:
        bits.append(k % 2)
        k /= 2
    r = 1
    for bit in reversed(bits):
        r = r * r % p
        if bit == 1:
            r = r * a % p
    return r

def solve():
    N = 10 ** 6
    p = 1000000007
    r = 0
    for k in range(1, N+1):
        if k % 1000 == 0:
            print k
        k2 = k * k % p
        k2i = modInv(k2, p)
        acc = k2 + p - 1
        acc = acc * (modPow(k2 + p - 1, N, p) + p - 1)
        acc = acc % p
        acc = acc * k2i % p
        r += acc
        r = r % p
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
