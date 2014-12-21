def genConfig(n = 1500):
    """
    Generates the initial config corresponding to the actual
    ProjectEuler #334 problem (which uses n = 1500)
    """
    r = []
    t = 123456
    for i in range(0, n):
        isOdd = t % 2 == 1
        t = t / 2
        if isOdd:
            t = t ^ 926252
        r.append((t % 2048) + 1)
    return r

def solve():
    # We make use of the following 3 'invariants':
    # \sum _k c[k] is constant, C0
    # \sum _k k * c[k] is constant, C1
    # \sum _k k^2 * c[k] increases by 2 at every individual spill, so of the form C2+2n
    # where n is the total number of spills from the initial configuration
    #
    # On top of that, we use the fact that a final configuration contains only
    # contiguous 1's and at most one zero in between them
    #
    # If we assume the configuration starts at index -s, ends at index e, with a single zero
    # at index e-h (hole) (between 1-s and e), then:
    # * e + s = C0
    # * \sum _{k=-s}^e k - e + h = C1
    #
    # this gives:
    # 2h = 2C1 + C0(C0 - 2e + 1)
    c = genConfig()
    C0 = 0
    C1 = 0
    C2 = 0
    for k in range(0, 1500):
        C0 += c[k]
        C1 += k * c[k]
        C2 += k * k * c[k]
    # C0 is even, h is equal to C1 mod C0/2, which gives two possible values
    # for h. However, since C0 and C1 are both 0 modulo 4, then h must be 2 mod 4
    C0half = C0 / 2
    h1 = C1 % C0half
    h2 = h1 + C0half
    # only h2 is 0 mod 4:
    h  = h2
    e = (2 * C1 + C0 * C0 + C0 - 2 * h ) / ( 2 * C0)
    s = C0 - e
    # The above is the final configuration, we compute C2final:
    C2final = 0
    for k in range(-s, e+1):
        C2final += k * k
    C2final -= (e-h)*(e-h)
    result = (C2final - C2) / 2
    return result

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
