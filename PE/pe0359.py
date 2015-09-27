def s2(n):
    return n * (n + 1) * (2 * n + 1) / 6

def s2Alt(n):
    # n^2 - (n-1)^2 + (n-2)^2...
    r = 8 * s2(n/2) - s2(n)
    if r < 0:
        r = -r
    return r

def P(f, r):
    if f == 1:
        return s2Alt(r)
    fh = f / 2
    result = s2Alt(2 * fh + r - 1) - fh
    if ( r + f ) % 2 == 0:
        result += 2 * fh
    return result

# Very naive function (used for investigating/checking)
def hilbertLocate(k):
    last = dict()
    r    = []
    for n in range(1, k+1):
        f = 1
        done = False
        while not done:
            m = last.get(f, None)
            if m == None:
                r.append((f, 1))
                last[f] = (n, 1)
                done = True
            else:
                if isSquare(m[0]+n):
                    r.append((f, m[1]+1))
                    last[f] = (n, m[1]+1)
                    done = True
            f += 1
    return r

def solve():
    # the number is 2^27 * 3^12
    n = 2 ** 27 * 3 ** 12
    acc = 0
    for a in range(0, 28):
        a2 = 2 ** a
        for b in range(0, 13):
            f = a2 * 3 ** b
            r = n / f
            acc += P(f, r)
    return acc

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
