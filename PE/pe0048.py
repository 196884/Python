def powMod(a, b, m):
    a2k    = a # a^(2^k)
    result = 1
    while b > 0:
        if b % 2 == 1:
            result = (result * a2k) % m
        a2k = (a2k * a2k) % m
        b /= 2
    return result

def solve():
    result = 0
    m = 10 ** 10
    for k in range(1, 1001):
        result = (result + powMod(k, k, m)) % m
    return result
    
if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

