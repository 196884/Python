def solve():
    l = [1]
    for n in range(0, 1000):
        rem = 0
        l2 = []
        for x in l:
            rem += 2 * x
            l2.append(rem % 10)
            rem = rem / 10
        while rem > 0:
            l2.append(rem % 10)
            rem = rem / 10
        l = l2
    return sum(l)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

