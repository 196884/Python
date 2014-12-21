import array

def solve():
    """ 
    Returns all prime numbers <= n via Eratosthene's sieve
    """
    result = 0
    n = 2000000
    sieve = array.array('i', (True for i in range(0, n)))
    for k in range(2, n):
        if sieve[k]:
            result += k
            i = k * k
            while i < n:
                sieve[i] = False
                i += k
    return result

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result



