# We use generating functions (working modulo x^200)

def product(l1, l2):
    n = len(l1)
    r = [0 for i in range(0, n)]
    for i in range(0, n):
        x1 = l1[i]
        j = 0
        while i + j < n:
            r[i+j] += x1 * l2[j]
            j += 1
    return r

def solve():
    n = 201
    r = [0 for i in range(0, n)]
    r[0] = 1
    values = [1, 2, 5, 10, 20, 50, 100, 200]
    for v in values:
        lv = [0 for i in range(0, n)]
        i = 0
        while i < n:
            lv[i] = 1
            i += v
        r = product(r, lv)
    return r[-1]

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result


