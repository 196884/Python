def sortedDigits(n):
    l = []
    while n > 0:
        l.append(n%10)
        n /= 10
    l.sort()
    return l

def solve():
    # Starting naive, you never know!
    # it has to start with a 1, because of the 6 multiple (total nb of digits must remain the same)
    basis = 1
    while True:
        basis *= 10
        for tail in range(0, basis):
            n = basis + tail
            l = sortedDigits(n)
            k = 2
            nk = n
            while k <= 6:
                nk += n
                if l != sortedDigits(nk):
                    k = 10
                k += 1
            if k == 7:
                return n

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

