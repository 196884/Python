
def countLosingUpTo(n):
    r = 0
    if n >= 1:
        r += 1
    if n >= 15:
        r += 1
    if n >= 35:
        r += 1
    r += 5 * (n / 34)
    q = n % 34
    if q >= 5:
        r += 1
    if q >= 9:
        r += 1
    if q >= 21:
        r += 1
    if q >= 25:
        r += 1
    if q >= 29:
        r += 1
    return r

def solve():
    n = 10 ** 6
    return n - countLosingUpTo(n)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
