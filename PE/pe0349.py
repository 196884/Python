def simulate(n, k):
    g = []
    l = [0 for z in range(0, n)]
    for z in range(0, n):
        g.append(list(l))
    i = n / 2
    j = n / 2
    d = 0
    nb = 0
    nbs = []
    for s in range(0, k):
        if g[i][j] == 1:
            d = (d - 1) % 4
            nb -= 1
        else:
            d = (d + 1) % 4
            nb += 1
        nbs.append(nb)
        g[i][j] = 1 - g[i][j]
        if d == 0:
            j += 1
        elif d == 1:
            i += 1
        elif d == 2:
            j -= 1
        else:
            i -= 1
    return (nbs[-1], nbs[-1]-nbs[-105])

def solve():
    # It eventually becomes periodic with a period of 104, adding 12 by period
    a = 104040
    n = 10 ** 18 - a
    (b, r) = simulate(2000, a)
    return b + n * r / 104

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
