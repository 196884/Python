# Misc. functions to work on the 'Spilling the Beans' problem,
# communicated by Zach, but originally from Project Euler
# (Problem #334), see:
#
# https://projecteuler.net/problem=334
#
# Also using this as a pretext to do some Python, very early steps!

def iterateSingle(l):
    """
    Does a *single* spill (2 beans going to the 2 neighbors), picking
    the leftmost spillable bin

    Keyword argument:
    l -- the expanded bean configuration
    """
    res = l
    for i in range(0, len(l)):
        if res[i] > 1:
            res[i  ] -= 2
            res[i-1] += 1
            res[i+1] += 1
            return res
    return res


def iterateCount(l, n):
    """
    Applies iterateSingle a specified number of times

    Keyword arguments:
    l -- the expanded bean configuration
    n -- the number of iterations to do
    """
    for i in range(0, n):
        l = iterateSingle(l)
    return l


def iterate(l):
    """ 
    Does a one-step bean spilling iteration (each position is
    expanded to the maximum).

    Returns a couple (result configuration, #spills) 

    Keyword argument:
    l -- the list containing the expanded bean configuration
    """
    res = []
    p = 0
    pp = 0
    n = 0
    first = True
    for x in l:
        q = 0
        r = x
        if x >= 2:
            q = int(x/2)
            r = int(x%2)
        if not first or q > 0:
            res.append(pp+q)
        first = False
        n += q
        pp = p + r
        p = q
    res.append(pp)
    if p > 0:
        res.append(p)
    return (res, n)


def f2(a, b):
    """ 
    Closed form number of spills for a configuration of the form
    1^a 2^b 1^a

    Keyword arguments:
    a -- as above
    b -- as above
    """
    r = b % 2
    n = (b + 1) / 2
    res = 2*n*n*n + 3*a*n*n + a*a*n
    if r == 1:
        res = res - n*n - a*n
    return res


def iterateAll(l):
    """
    Successively applies 'iterate' until a stable configuration is found.

    Returns a couple (final configuration, total #spills)
    
    Keyword argument:
    l -- the initial expanded bean configuration
    """
    r = 0
    (l, n) = iterate(l)
    while n > 0:
        r += n
        (l, n) = iterate(l)
    return (l, r)


def decompress(l):
    """
    Given a bean configuration encoded in the form:
    [(n_0, v_0), (n_1, v_1),... ]
    expands it as:
    [ v_0 (n_0 times), v_1 (n_1 times),... ]
    """
    res = []
    for (a, b) in l:
        for i in range(0, a):
            res.append(b)
    return res


def compress(l):
    """
    Inverse operation of decompress
    """
    res = []
    prev = 0
    count = 0
    for x in l:
        if prev == x:
            count +=1
        else:
            res.append((count, prev))
            count = 1
            prev  = x
    res.append((count, prev))
    return res


def f2t(a, b):
    """
    Utility function to investigate how configurations of
    the form
    1^a 2^b 1^a
    expand
    """
    x = decompress([(a, 1), (b, 2), (a, 1)])
    (l, n) = iterateAll(x)
    return n


def f3t(a, b, c):
    """
    Utility function to investigate how configurations of
    the form
    1^a 2^b 1^c
    expand
    """
    x = decompress([(a, 1), (b, 2), (c, 1)])
    (l, n) = iterateAll(x)
    return n


def T(a, b):
    """
    Expands a number encoded in triangular form

    Keyword arguments:
    a -- the index of the triangular number
    b -- the remainder (b <= a)
    """
    return a*(a+1)/2+b

def s(a, b):
    """
    The cost function to expand T(a, b)
    under the form
    e_0, e_1, ..., e_a, T(a-1, b)
    where e_i = 1 for i != b and e_b = 0
    """
    return a*(a*a-1)/6 + a*b - b*(b-1)/2


def Tinv(x, lower = 0):
    """
    Finds a and b (b <= a) such that
    x = T(a, b)

    Keyword values:
    x -- the number to invert
    lower -- to optimize, a lower bound for a
    """
    a = lower
    t = lower * ( lower + 1 ) / 2
    if x < lower:
        a = 0
        t = 0
    while x - t > a:
        a += 1
        t += a
    return (a, x - t)


def genConfig(n = 1500):
    """
    Generates the initial config corresponding to the actual
    ProjectEuler #334 problem (which uses n = 1500)
    """
    r = []
    t = 123456
    for i in range(0, n):
        isOdd = t % 2 == 1
        t = t / 2
        if isOdd:
            t = t ^ 926252
        r.append((t % 2048) + 1)
    return r


def solve(n = 1500):
    """
    Finds the solution
    """
    config = genConfig(n)
    prevA = 0
    prevB = 0
    r     = 0
    p     = 0
    steps = 0
    while r >= 1 or p < n:
        # At this point, the configuration is of the form:
        # e_0, e_1, ...., e_prevA, r
        # where:
        # * r is at position p on the grid
        # * e_i = 1 for i != b, and e_b = 0
        # * the elements of config of index >= p are added on top
        #   of the above
        if p % 10000 == 0:
            print "p: %d, r: %d, steps: %d" % (p, r, steps)
        if p < n:
            r += config[p]
        q = T(prevA, prevB) + r
        (a, b) = Tinv(q, lower = prevA)
        incSteps = s(a, b) - s(prevA, prevB)
        rDec = a - prevA + 1
        prevA = a + 1
        prevB = b
        steps += incSteps
        r -= rDec
        p += 1
    return steps


