def toHex(n):
    l = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F" ]
    r = ""
    while n > 0:
        c = l[n % 16]
        r = c + r
        n /= 16
    return r

def aux(m, r):
    if r == 0:
        return m[0]
    m2 = [
        16 * m[0] + m[1] + m[2] + m[3],
        15 * m[1] + m[4] + m[6],
        15 * m[2] + m[4] + m[5],
        15 * m[3] + m[5] + m[6],
        14 * m[4] + m[7],
        14 * m[5] + m[7] + 1,
        14 * m[6] + m[7] + 1,
        13 * m[7] + 13
    ]
    return aux(m2, r-1)

def solve():
    s = aux([0, 0, 0, 0, 0, 0, 0, 0], 16)
    return toHex(s)

if __name__ == "__main__":
    # States:
    # 0: seen everything
    # 1: seen 0 and 1
    # 2: seen 0 and A
    # 3: seen 1 and A
    # 4: seen only 0 (and other stuff before)
    # 5: seen only A
    # 6: seen only 1
    # 7: seen other digits only
    # (we don't even factor out the 1/A symmetry, could be done)
    result = solve()
    print "Result: %s" % result
