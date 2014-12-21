def isPalindromic(n, k):
    """
    Tests whether n is palindromic in base k:
    """
    aux = n
    x = 0
    while aux > 0:
        x = k * x + aux % k
        aux /= k
    return x == n

def toBinary(n):
    r = []
    while n > 0:
        r.append(n % 2)
        n /= 2
    return list(reversed(r))

def solve():
    # it would be faster to generate the palindromes in base 10, but
    # whatever
    result = 0
    for n in range(1, 1000000):
        if isPalindromic(n, 10) and isPalindromic(n, 2):
            result += n
    return result

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
