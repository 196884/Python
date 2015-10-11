def ulamFn(v, k):
    # Using results from Finch 'On the Regularity of Certain 1-Additive Sequences'
    p = (v+1)/2
    beta0 = 2 ** v
    beta = beta0 / 2 + beta0
    prev = 1
    n = p + 1
    r = 0
    l = [2, v, 2+v]
    evenDone = False
    while beta != beta0:
        curr  = (prev + beta) % 2
        beta /= 2
        if curr == 1:
            beta += beta0
            r += 1
            prev = 1
            if not evenDone and 2 * v + 2 < 2 * n + 1:
                l.append(2*v+2)
                evenDone = True
            l.append(2*n+1)
        else:
            prev = 0
        n += 1
    q = n
    D = 2 * (q - p)
    N = r + 1
    k -= 1 # our list is indexed starting at 0...
    if k < len(l):
        return l[k]
    kRed = k % N
    if kRed == 1:
        kRed = N + 1
        k -= N
    elif kRed == 0:
        kRed = N
        k -= N
    elif kRed <= v:
        kRed -= 1
    return l[kRed] + (k / N) * D

def solve():
    k = 10**11
    r = 0
    for n in range(2, 11):
        r += ulamFn(2*n+1, k)
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
