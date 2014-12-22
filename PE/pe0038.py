# We can look for k < 10^5
def check(n):
    b = [False for i in range(0, 10)]
    b[0] = True
    while n > 0:
        d = n % 10
        if b[d]:
            return False
        b[d] = True
        n /= 10
    return len(set(b)) == 1

def nbDigits(n):
    r = 0
    while n > 0:
        r += 1
        n /= 10
    return r

def solve():
    result = 0
    for n in range(1, 100000):
        totalDigits = nbDigits(n)
        curr = n
        k = 1
        while totalDigits < 9:
            k += 1
            aux = k * n
            nbd = nbDigits(aux)
            curr = curr * 10 ** nbd + aux
            totalDigits += nbd
        if 9 == totalDigits and check(curr):
            result = max(result, curr)
    return result

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
