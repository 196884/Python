# We use Pythagorean triples:
# a = n^2 - m^2
# b = 2mn
# c = n^2 + m^2
# m < n

def solve():
    l = [set() for i in range(0, 1001)]
    # This set thing is pretty inefficient, better to make sure we generate each one
    # only once
    for m in range(1, 999):
        m2 = m * m
        for n in range(m+1, 1000):
            n2 = n * n
            a = n2 - m2
            b = 2 * m * n
            c = n2 + m2
            pb = a+b+c
            if b < a:
                x = b
                b = a
                a = x
            k = 1
            while k * pb <= 1000:
                l[k*pb].add(k * (1000000 * a + 1000 * b + c))
                k += 1
    r = 0
    m = 0
    for i in range(0, 1001):
        x = len(l[i])
        if x > m:
            m = x
            r = i
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

