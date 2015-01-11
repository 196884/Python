def sumDigits(n):
    r = 0
    while n > 0:
        r += n % 10
        n /= 10
    return r

def solve():
    # The simplest is to generate them: if we want all the numbers n<10^b,
    # then the sum of their digits is less than 9b, so not that many powers...
    b = 20
    B = 10 ** 20
    s = set()
    for sd in range(2, 9 * b + 1):
        sdPower = sd
        while sdPower < B:
            sdPower *= sd
            if sumDigits(sdPower) == sd:
                s.add(sdPower)
    l = list(s)
    l.sort()
    return l[29]

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
