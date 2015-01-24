def aux(l):
    r = 0.0
    if 0 == sum(l):
        return r
    if 1 == sum(l):
        r += 1.0
    n = sum(l)
    for i, k in enumerate(l):
        if k > 0:
            ll = list(l)
            ll[i] -= 1
            for j in range(i+1, 5):
                ll[j] += 1
            r += aux(ll) * float(k) / float(n)
    return r

def solve():
    r = aux([1, 0, 0, 0, 0]) - 2
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %s" % str(result)
