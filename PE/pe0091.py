def gcd(a, b):
    if b > a:
        return gcd(b, a)
    if b == 0:
        return a
    return gcd(b, a%b)

def solve():
    # There are 2 kinds of right triangle:
    # * right angle at the origin: clearly, M^2 of these
    # * right angle at a point (a, b). In this case, if we write a = g.x and b = g.y
    #   where g is the gcd of a and b, then the solutions for the third point are parametrized as:
    #   (a - k.y, b + k.x) for k any integer
    #   Since we want the third point in the square as well, this just adds upper and lower bounds on k,
    #   so we can simply apply these bounds and count
    M = 50
    r = M ** 2
    for a in range(0, M+1):
        for b in range(0, M+1):
            if a + b > 0:
                g = gcd(a, b)
                x = a / g
                y = b / g
                if x == 0:
                    kMax = a / y
                    kMin = (a-M) / y
                    if (a-M) % y != 0:
                        kMin += 1
                elif y == 0:
                    kMax = (M-b) / x
                    kMin = -b / x
                    if b % x != 0:
                        kMin += 1
                else:
                    kMax = min(a / y, (M-b) / x)
                    aux1 = -b / x
                    if b % x != 0:
                        aux1 += 1
                    aux2 = (a-M) / y
                    if (a-M) % y != 0:
                        aux2 += 1
                    kMin = max(aux1, aux2)
                r += kMax - kMin
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
