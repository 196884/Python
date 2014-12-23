def admissible3(n):
    a = n % 10
    n /= 10
    b = n % 10
    n /= 10
    c = n %10
    n /= 10
    return n == 0 and a != b and a !=c and b != c

def possiblePrefixes(p, r):
    result = []
    for k in range(0, 10):
        if (100 * k + r) % p == 0:
            result.append(k)
    return result

def toInt(l):
    r = 0
    for x in l:
        r = 10 * r + x
    return r

def solve():
    # not very nice... anyways, fast and quick to code
    result = 0
    suffixes = []
    k = 1000 / 17
    for m in range(1, k+1):
        m17 = 17 * m
        if admissible3(m17):
            a17 = (m17 / 100) % 10
            b17 = (m17 / 10) % 10
            c17 = m17 % 10
            ds17 = set([a17, b17, c17])
            r = m17 / 10
            p13s = possiblePrefixes(13, r)
            for p13 in p13s:
                if p13 not in ds17:
                    ds13 = set(ds17)
                    ds13.add(p13)
                    r = 10 * p13 + (m17 / 100) % 10
                    p11s = possiblePrefixes(11, r)
                    for p11 in p11s:
                        if p11 not in ds13:
                            ds11 = set(ds13)
                            ds11.add(p11)
                            r = 10 * p11 + p13
                            p7s = possiblePrefixes(7, r)
                            for p7 in p7s:
                                if p7 not in ds11:
                                    ds7 = set(ds11)
                                    ds7.add(p7)
                                    r = 10 * p7 + p11
                                    p5s = possiblePrefixes(5, r)
                                    for p5 in p5s:
                                        if p5 not in ds7:
                                            ds5 = set(ds7)
                                            ds5.add(p5)
                                            r = 10 * p5 + p7
                                            p3s = possiblePrefixes(3, r)
                                            for p3 in p3s:
                                                if p3 not in ds5:
                                                    ds3 = set(ds5)
                                                    ds3.add(p3)
                                                    r = 10 * p3 + p5
                                                    p2s = possiblePrefixes(2, r)
                                                    for p2 in p2s:
                                                        if p2 not in ds3:
                                                            ds2 = set(ds3)
                                                            ds2.add(p2)
                                                            for p1 in range(0, 10):
                                                                if p1 not in ds2:
                                                                    result += toInt([p1, p2, p3, p5, p7, p11, p13, a17, b17, c17])
    return result

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

