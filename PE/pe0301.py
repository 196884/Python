def solve():
    # a quick case study shows:
    # 1 -> 2
    # 2 -> 3
    # f(k) = f(k-1) + f(k-2)
    # (key is to verify that n = 4k+3 cannot work)
    l = [ 2, 3 ]
    n = 2
    while n < 30:
        l.append(l[-1]+l[-2])
        n += 1
    return l[-1]

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
