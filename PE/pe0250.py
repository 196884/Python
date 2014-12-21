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
    m = 250
    mm = 10 ** 16
    l = [0 for i in range(0, m)]
    # l[i] is the number of sets of sum i mod m with all elements up to n
    l[0] = 1
    for n in range(1, 250251):
        prevL = list(l)
        nm = powMod(n, n, m)
        # either we include nm or we don't:
        for i in range(0, m):
            j = (nm + i) % m
            l[j] = (l[j] + prevL[i]) % mm
    return l[0] - 1
   
if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

