from mpmath import *

mp.dps = 22

N = 30
N2 = N * N

cache = dict()

def density(i, j, k):
    # density function starting at (i, j) and jumping k times:
    cached = cache.get((i, j, k), None)
    if cached != None:
        return cached
    if k == 0:
        r = [ mpf(0) for z in range(0, N2)]
        r[i + N * j] = mpf(1)
    else:
        r = [ mpf(0) for z in range(0, N2)]
        b = mpf(0)
        if j > 0:
            b += 1
            aux = density(i, j-1, k-1)
            for z in range(0, N2):
                r[z] += aux[z]
        if j < N-1:
            b += 1
            aux = density(i, j+1, k-1)
            for z in range(0, N2):
                r[z] += aux[z]
        if i > 0:
            b += 1
            aux = density(i-1, j, k-1)
            for z in range(0, N2):
                r[z] += aux[z]
        if i < N-1:
            b += 1
            aux = density(i+1, j, k-1)
            for z in range(0, N2):
                r[z] += aux[z]
        for z in range(0, N2):
            r[z] /= mpf(b)
    cache[(i, j, k)] = r
    if k >= 20:
        print (i, j, k, len(cache))
    return r

def solve():
    n = mpf(0)
    for i in range(0, N):
        for j in range(0, N):
            print (i, j)
            acc = mpf(1)
            for a in range(0, N):
                for b in range(0, N):
                    aux = density(a, b, 50)
                    acc *= mpf(1) - aux[i + N * j]
            n += acc
    print n
    return 0

if __name__ == "__main__":
    # could use symmetry,... to speed up, but this works
    result = solve()
    print "Result: %d" % result
