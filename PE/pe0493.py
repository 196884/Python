from mpmath import *

mp.dps = 30

def sortFn((a, b)):
    return a

def evolvePos(c, i):
    # c is the configuration
    # i is the index chosen
    r = list(c)
    (ni, ki) = c[i]
    f = ni * ki
    if ki > 1:
        r[i] = (ni, ki-1)
    else:
        r.pop(i)
    if ni > 1:
        n = len(r)
        found = False
        for i in range(0, n):
            if r[i][0] == ni - 1:
                r[i] = (r[i][0], r[i][1]+1)
                found = True
        if not found:
            r.append((ni-1, 1))
            r.sort(key = sortFn)
    return (f, tuple(r))

def handlePick(d, total):
    r = dict()
    for c, proba in d.iteritems():
        nc = len(c)
        for i in range(0, nc):
            (f, cb) = evolvePos(c, i)
            thisProba = proba * mpf(f) / mpf(total)
            prevProba = r.get(cb, mpf(0))
            r[cb] = prevProba + thisProba
    return r

def nbColors(c):
    l = list(c)
    (n, k) = l[-1]
    if n == 10:
        return 7 - k
    else:
        return 7
           
def solve():
    # Bruteforcing it...
    d = dict()
    d[((9,1),(10,6))] = mpf(1)
    total = 69
    for k in range(0, 19):  
        d = handlePick(d, total)
        total -= 1
    r = mpf(0)
    for c, p in d.iteritems():
        n = nbColors(c)
        r = r + mpf(n) * p
    return r
  
if __name__ == "__main__":
    result = solve()
    print "Result: %s" % result
