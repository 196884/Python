import array

def solve():
    M = 2**50
    B = 2**25
    sieve = array.array('i', (0 for i in range(0, B+1)))
    # We count the numbers that have squares...
    r = 0
    for k in range(2, B+1):
        if k < 1000 or k % 1000 == 0:
            print (k, B)
        if sieve[k] == 0:
            # k is prime
            r += M / (k * k)
            km = k
            while km <= B:
                sieve[km] += 1
                km += k
        elif sieve[k] > 1:
            r -= (sieve[k] - 1) * (M / (k*k))
            s = sieve[k] - 1
            km = k
            while km <= B:
                sieve[km] -= s
                km += k
    return M - r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
