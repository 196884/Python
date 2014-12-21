# Done by hand, using the decomposition:
# 999999 = 2.9! + 6.8! + 6.7! + 2.6! + 5.5! + 1.4! + 2.3! + 1.2! + 1.1!

def fact(n):
    r = 1
    for k in range(2, n+1):
        r *= k
    return r

def solve():
    return 2783915460

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

