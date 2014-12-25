def reverse(n):
    r = 0
    while n > 0:
        r = 10 * r + n % 10
        n /= 10
    return r

def isLychrel(n):
    n += reverse(n) # a palyndrome is not automatically considered non-Lychrel...
    for i in range(0, 50):
        r = reverse(n)
        if r == n:
            return False
        n += r
    return True

def solve():
    r = 0
    for n in range(1, 10000):
        if isLychrel(n):
            r += 1
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

