def solve():
    # Yet another pretty naive one...
    B = 50 * 10 ** 6
    isPrime = [True for n in range(0, B+1)]
    r = 0
    for n in range(2, B+1):
        if isPrime[n]:
            p = n
            pk = 2 * p
            while pk <= B:
                isPrime[pk] = False
                pk += p
            if 4 * p <= B:
                r += 1
            if 16 * p <= B:
                r += 1
            if p % 4 == 3:
                r += 1
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
