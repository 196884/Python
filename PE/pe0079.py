data = [
    319,
    680,
    180,
    690,
    129,
    620,
    762,
    689,
    762,
    318,
    368,
    710,
    720,
    710,
    629,
    168,
    160,
    689,
    716,
    731,
    736,
    729,
    316,
    729,
    729,
    710,
    769,
    290,
    719,
    680,
    318,
    389,
    162,
    289,
    162,
    718,
    729,
    319,
    790,
    680,
    890,
    362,
    319,
    760,
    316,
    729,
    380,
    319,
    728,
    716
]

def possibleLastDigits(s):
    sLast = set()
    for n in s:
        sLast.add(n%10)
    r = set()
    for d in sLast:
        sAux = set()
        for n in s:
            if n % 10 == d:
                n /= 10
            while n > 0:
                sAux.add(n % 10)
                n /= 10
        if d not in sAux:
            r.add(d)
    return r



def solve():
    # Naive: check whether there's a solution with at most
    # one appearance of each digit... and there's one unique solution :)
    s   = set(data)
    r   = 0
    p10 = 1
    while len(s) > 0:
        possibles = possibleLastDigits(s)
        if len(possibles) != 1:
            return 0
        # so we found the optimal suffix:
        d = list(possibles)[0]
        r += p10 * d
        p10 *= 10
        sNew = set()
        for n in s:
            if n % 10 == d:
                n /= 10
            if n > 0:
                sNew.add(n)
        s = sNew
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
