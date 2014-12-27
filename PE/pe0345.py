data = [
    [   7,  53, 183, 439, 863],
    [ 497, 383, 563,  79, 973 ],
    [ 287,  63, 343, 169, 583],
    [ 627, 343, 773, 959, 943],
    [ 767, 473, 103, 699, 303]
]

data2 = [
    [  7,  53, 183, 439, 863, 497, 383, 563,  79, 973, 287,  63, 343, 169, 583 ],
    [627, 343, 773, 959, 943, 767, 473, 103, 699, 303, 957, 703, 583, 639, 913 ],
    [447, 283, 463,  29,  23, 487, 463, 993, 119, 883, 327, 493, 423, 159, 743 ],
    [217, 623,   3, 399, 853, 407, 103, 983,  89, 463, 290, 516, 212, 462, 350 ],
    [960, 376, 682, 962, 300, 780, 486, 502, 912, 800, 250, 346, 172, 812, 350 ],
    [870, 456, 192, 162, 593, 473, 915,  45, 989, 873, 823, 965, 425, 329, 803 ],
    [973, 965, 905, 919, 133, 673, 665, 235, 509, 613, 673, 815, 165, 992, 326 ],
    [322, 148, 972, 962, 286, 255, 941, 541, 265, 323, 925, 281, 601,  95, 973 ],
    [445, 721,  11, 525, 473,  65, 511, 164, 138, 672,  18, 428, 154, 448, 848 ],
    [414, 456, 310, 312, 798, 104, 566, 520, 302, 248, 694, 976, 430, 392, 198 ],
    [184, 829, 373, 181, 631, 101, 969, 613, 840, 740, 778, 458, 284, 760, 390 ],
    [821, 461, 843, 513,  17, 901, 711, 993, 293, 157, 274,  94, 192, 156, 574 ],
    [ 34, 124,   4, 878, 450, 476, 712, 914, 838, 669, 875, 299, 823, 329, 699 ],
    [815, 559, 813, 459, 522, 788, 168, 586, 966, 232, 308, 833, 251, 631, 107 ],
    [813, 883, 451, 509, 615,  77, 281, 613, 459, 205, 380, 274, 302,  35, 805 ]
]

def score(p, l):
    n = len(l)
    result = sum([l[p[i]][i] for i in range(0, n)])
    return result

def genCycles(n):
    r = []
    b = 2 ** n
    for n in range(1, b):
        l = []
        a = n
        i = 0
        while a > 0:
            if a % 2 == 1:
                l.append(i)
            a /= 2
            i += 1
        if len(l) > 1:
            r.append(l)
    return r

def compose(p, c, k):
    # c is a cycle, we compute p o c^k
    r = list(p)
    n = len(c)
    aux = p[c[k]]
    for i in range(1, n):
        r[c[i]] = p[c[(i+k) % n]]
    r[c[0]] = aux
    return r

def solve():
    # p is the current permutation
    # another pretty naive, non optimized approach
    # we simply use the decomposition in cycles:
    # if we are in a suboptimal configuration, a cycle can improve it
    p = [i for i in range(0, 15)]
    maxScore = score(p, data2)
    cycles = genCycles(len(p))
    nbCycles = len(cycles)
    found = True
    while found:
        found = False
        ci = 0
        while not found and ci < nbCycles:
            c = cycles[ci]
            cn = len(c)
            cii = 1
            while not found and cii < cn:
                pt = compose(p, c, cii)
                ps = score(pt, data2)
                if ps > maxScore:
                    maxScore = ps
                    p = pt
                    found = True
                    print "Max: %d" % maxScore
                    print p
                cii += 1
            ci += 1
    return maxScore

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
