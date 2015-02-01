def solve():
    # First solutions found by exhaustive search
    l = [(17, 7), (32, 14), (112, 50), (217, 97), (767, 343), (1487, 665)]
    for k in range(6, 30):
        v = l[-6]
        v0 = 161 * v[0] + 360 * v[1]
        v1 = 72 * v[0] + 161 * v[1]
        l.append((v0, v1))
    return sum([(v[0]+8)/5 - 3for v in l])

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
