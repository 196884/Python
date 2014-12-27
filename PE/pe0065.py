def solve():
    l = [2]
    for k in range(1, 34):
        l.append(1)
        l.append(2*k)
        l.append(1)
    l = list(reversed(l))
    n = l[0]
    d = 1
    l = l[1:]
    for x in l:
        aux = n
        n = n * x + d
        d = aux
    r = 0
    while n > 0:
        r += n % 10
        n /= 10
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
