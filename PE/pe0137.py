def solve():
    l = [(11, 5), (76, 16), (521, 233)]
    k = 3
    for k in range(4, 16):
        v = l[-3]
        v0 = 161 * v[0] + 360 * v[1]
        v1 = 72 * v[0] + 161 * v[1]
        l.append((v0, v1))
    return (l[-1][0] - 1) / 5

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
