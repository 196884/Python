def getNthDigit(n):
    n    -= 1
    k     = 0
    power = 1 # 10^k
    thisRangeLength = 9 * (k + 1) * power
    while n >= thisRangeLength:
        n -= thisRangeLength
        k += 1
        power *= 10
        thisRangeLength = 9 * (k + 1) * power
    q = n / (k + 1)
    r = n % (k + 1)
    x = power + q
    result = (x / 10 ** (k-r)) % 10
    return result

def solve():
    r = 1
    p = 1
    k = 0
    while k <= 6:
        r *= getNthDigit(p)
        p *= 10
        k += 1
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
