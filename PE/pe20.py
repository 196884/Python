def multList(l, n):
    result = []
    rem = 0
    for d in l:
        rem += d * n
        result.append(rem % 10)
        rem /= 10
    while rem > 0:
        result.append(rem % 10)
        rem /= 10
    return result

def factList(n):
    result = [1]
    for k in range(2, n+1):
        result = multList(result, k)
    return result

def solve():
    l = factList(100)
    r = sum(l)
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
