def solve():
    b = 1000000
    factors = [0 for i in range(0, b)]
    for n in range(2, b):
        if factors[n] == 0:
            # n is prime:
            k = 1
            nk = n
            while nk < b:
                factors[nk] += 1
                nk += n
    for n in range(2, b-3):
        if min([factors[n], factors[n+1], factors[n+2], factors[n+3]]) >= 4:
                return n
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
