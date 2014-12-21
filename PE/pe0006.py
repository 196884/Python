def sumOfSquares(n):
    result = n * (n + 1) * (2 * n + 1) / 6
    return result

def solve():
    n = 100
    s = n * (n + 1) / 2
    r = s * s - sumOfSquares(n)
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
