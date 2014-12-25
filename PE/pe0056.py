def digitSum(n):
    r = 0
    while n > 0:
        r += n % 10
        n /= 10
    return r

def solve():
    # Naive...
    r = 0
    for a in range(2, 100):
        p = 1
        for b in range(1, 100):
            p *= a
            r = max(r, digitSum(p))
    return r
    
if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

