xMax = 32 
yMax = 10

cache = dict()

def aux(x, y, curr, prev):
    if y == 0:
        return 1
    if x > xMax or prev & 2 ** x:
        return 0
    if x == xMax:
        return aux(0, y-1, 0, curr)
    if x == 0:
        cached = cache.get((y, prev))
        if cached != None:
            return cached
        result = aux(x+2, y, curr, prev) + aux(x+3, y, curr, prev)
        cache[(y, prev)] = result
        return result
    result = aux(x+2, y, curr + 2**x, prev) + aux(x+3, y, curr + 2**x, prev)
    return result
    
def solve():
    r = aux(0, yMax, 0, 0)
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
