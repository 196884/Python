import itertools as it

def solve():
    primes = []
    # keyed by size and then set of digits
    nb = 6
    b = 10 ** nb 
    sieve = [True for i in range(0, b)]
    for n in range(2, b):
        if sieve[n]:
            # n is prime
            p = n
            primes.append(p)
            if len(primes) % 2 == 1 and 2 * len(primes) * p  > 10 ** 10:
                return len(primes) 
            mp = p
            while mp < b:
                sieve[mp] = False
                mp += p
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

