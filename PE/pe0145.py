def countAux(n):
    """
    Returns (r_e_nc, r_o_nc, r_e_c, r_o_c)
    e/o:  even     / odd
    nc/c: no carry / carry
    """
    if n == 0:
        return (0, 1, 1, 0)
    if n == 1:
        return (5, 0, 5, 0)
    (n_e_nc, n_o_nc, n_e_c, n_o_c) = countAux(n-2)
    return (25 * n_o_c, 30 * n_o_nc, 25 * n_e_c, 20 * n_e_nc)

def count(n):
    (n_e_nc, n_o_nc, n_e_c, n_o_c) = countAux(n)
    # We need to remove leading zeros...
    return n_o_c + 2 * n_o_nc / 3
     
def solve():
    n = 9
    r = 0
    for k in range(1, n+1):
        r += count(k)
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
