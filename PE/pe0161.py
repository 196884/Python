nX = 12
nY = 9

def isFree(i, j, n):
    if n & ( 2 ** ( nY * i + j ) ) == 0:
        return True
    return False

def checkAndSet(l, n):
    for (i, j) in l:
        v = 2 ** ( nY * i + j )
        if n & v > 0:
            return 0
        n += v
    return n

cache = dict()
cache[(0, 0, 0)] = 1

# Shapes:
#
# a. #  b. ###  c. #   d.  #  e. ## f. ##
#    #             ##     ##     #      #
#    #
#
def aux(y, firstCols, nbRem):
    cached = cache.get((y, firstCols, nbRem), None)
    if cached != None:
        return cached
    if y >= nY:
        result = aux(0, firstCols / (2 ** nY), nbRem - 1)
    else:
        if isFree(0, y, firstCols):
            result = 0
            # a
            if y + 2 < nY:
                fcAux = checkAndSet([(0, y), (0, y+1), (0, y+2)], firstCols)
                if fcAux > 0:
                    result += aux(y+3, fcAux, nbRem)
            # b
            if nbRem >= 3:
                fcAux = checkAndSet([(0, y), (1, y), (2, y)], firstCols)
                if fcAux > 0:
                    result += aux(y+1, fcAux, nbRem)
            if nbRem >= 2 and y + 1 < nY:
                # c
                fcAux = checkAndSet([(0, y), (1, y), (0, y+1)], firstCols)
                if fcAux > 0:
                    result += aux(y+2, fcAux, nbRem)
                # d
                fcAux = checkAndSet([(0, y), (1, y), (1, y+1)], firstCols)
                if fcAux > 0:
                    result += aux(y+1, fcAux, nbRem)
                # e
                fcAux = checkAndSet([(0, y), (0, y+1), (1, y+1)], firstCols)
                if fcAux > 0:
                    result += aux(y+2, fcAux, nbRem)
            if y > 0 and nbRem >= 2:
                fcAux = checkAndSet([(0, y), (1, y), (1, y-1)], firstCols)
                if fcAux > 0:
                    result += aux(y+1, fcAux, nbRem)
        else:
            result = aux(y+1, firstCols, nbRem)
    cache[(y, firstCols, nbRem)] = result
    return result

def solve():
    # Straightforward DP
    r = aux(0, 0, nX)
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
