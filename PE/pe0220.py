def iterate(l):
    r = []
    for x in l:
        if x == 'F' or x == 'L' or x == 'R':
            r.append(x)
        else:
            if x == 'a':
                r.append('a')
                r.append('R')
                r.append('b')
                r.append('F')
                r.append('R')
            else:
                r.append('L')
                r.append('F')
                r.append('a')
                r.append('L')
                r.append('b')
    return r

def D(n):
    r = ['F', 'a']
    while n > 0:
        r = iterate(r)
        n -= 1
    return r

def positions(l):
    r = [(0,0)]
    d = 0
    for x in l:
        if x == 'F':
            (lx, ly) = r[-1]
            if d == 0:
                r.append((lx, ly+1))
            if d == 1:
                r.append((lx+1, ly))
            if d == 2:
                r.append((lx, ly-1))
            if d == 3:
                r.append((lx-1, ly))
        if x == 'L':
            d = (d + 3) % 4
        if x == 'R':
            d = (d + 1) % 4
    return r

def iter(((x, y), facing, isRight), piece):
    if piece == 0:
        pOut = (x + y, y - x)
        fOut = facing
        if isRight:
            fOut = (fOut + 1) % 4
        return (pOut, fOut, False)
    else:
        if isRight:
            fOut = facing
            facing = (facing + 1) % 4
        else:
            fOut = (facing + 1) % 4
        if facing == 0:
            pOut = (x+y, y-x+1)
        if facing == 1:
            pOut = (x+y+1, y-x)
        if facing == 2:
            pOut = (x+y, y-x-1)
        if facing == 3:
            pOut = (x+y-1, y-x)
        return (pOut, fOut, True)

def decompose(n):
    r = []
    while n > 0:
        r.append(n % 2)
        n = n / 2
    return list(reversed(r))

def pos(n):
    s = ((0, 0), 0, False)
    l = decompose(n)
    for b in l:
        s = iter(s, b)
    return s
               
def solve():
    return pos(10**12)[0]

if __name__ == "__main__":
    result = solve()
    print "Result: %d,%d" % result
