# this is path-dependent... since we can reuse intermediate results for free
# so we need to restart from scratch for each new exponent

def upperBound(n):
    r = 0
    while n > 0:
        if n % 2 == 1:
            r += 1
        r += 1
        n /= 2
    return r - 2

def minChainRec(target, ls, b):
    prefixes = []
    n = len(ls[0])
    if b == n:
        return b
    for l in ls:
        ll = l[-1]
        for d in l:
            lll = ll + d
            if lll == target:
                return n
            elif lll <= target and lll * (2 ** (b-n)) >= target:
                lRec = list(l)
                lRec.append(lll)
                prefixes.append(lRec)
    result = minChainRec(target, prefixes, b)
    return result

def solve():
    # We could also be looking for all of them at the same time, but this still isn't that slow
    r = 0
    for k in range(2, 201):
        x = minChainRec(k, [[1]], upperBound(k))
        r += x
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

