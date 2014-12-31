def powFloat(a, b, p):
    r = p
    a2k = a
    while b > 0:
        if b % 2 == 1:
            r = (r * a2k) / p
        a2k = (a2k * a2k) / p
        b /= 2
    return r

def solve():
    N = 10 ** 10
    M = N / 2
    N2 = N ** 2
    B = 4000
    precMult = 10 ** 10
    acc = 0
    k = M
    j = 0
    pB = precMult
    while pB > 0:
        num = 2 * M - k ** 2 - (k-1) ** 2
        p = 2 * precMult * num
        p /= N2
        pB = powFloat(p, B, precMult)
        acc += pB
        k -= 1
        j += 1
    r = M * precMult + acc
    r = r / (precMult / 100)
    r = "%d.%d" % (r / 100, r % 100)
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %s" % result
