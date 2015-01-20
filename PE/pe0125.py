def isPalindrome(n):
    s = str(n)
    l = list(s)
    return l == list(reversed(l))

def solve():
    d = set()
    b = 10 ** 8
    r = 0
    n = 1
    while n * n < b:
        s = n * n
        j = n + 1
        while s < b:
            s += j * j
            if s < b and isPalindrome(s):
                d.add(s)
                r += s
            j += 1
        n += 1
    return sum(d)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
