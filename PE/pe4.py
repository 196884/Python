# Largest palindrome made of 2 3-digit numbers
# Being lazy!

def solve():
    result = 0
    for i in range(100, 999):
        for j in range(100, 999):
            p = i * j
            s = "%d" % p
            if s == s[::-1]:
                result = max(result, p)
    return result

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
