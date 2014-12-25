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
    m = 10 ** 10
    x = powMod(2, 7830457, m) 
    x = (28433 * x + 1) % m
    return x

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

