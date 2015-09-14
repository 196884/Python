def solve():
    # Simple procedure:
    d = dict()
    for i in range(1, 10):
        for j in range(0, 10):
            if i + j < 10:
                d[ 10 * i + j ] = 1
    for a in range(3, 21):
        # handing the a-th digit:
        dd = dict()
        for prefix, nb in d.iteritems():
            d0 = prefix / 10
            d1 = prefix % 10
            d01 = d0 + d1
            for k in range(0, 10):
                if d01 + k < 10:
                    d1b = 10 * d1 + k
                    aux = dd.get(d1b, 0)
                    aux += nb
                    dd[d1b] = aux
        d = dd
    r = 0
    for x, y in d.iteritems():
        r += y
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
