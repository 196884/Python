def solve():
    l = [0 for k in range(0, 171)]
    oneDart = []
    for k in range(1, 21):
        for i in range(1, 4):
            oneDart.append((i, k))
    oneDart.extend([(1, 25), (2, 25)])
    doubles = [(2, k) for k in range(1, 21)]
    doubles.append((2, 25))
    # Finals in 1 dart:
    for (x, y) in doubles:
        l[x * y] += 1
    for (x1, y1) in oneDart:
        for (x2, y2) in doubles:
            l[x1*y1 + x2*y2] += 1
        for (x2, y2) in oneDart:
            if (x1, y1) <= (x2, y2):
                for (x3, y3) in doubles:
                    l[x1*y1 + x2*y2 + x3*y3] += 1
    return sum(l[:100])

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
