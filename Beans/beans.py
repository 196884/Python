# Misc. functions to work on the 'Spilling the Beans' problem,
# communicated by Zach, but originally from Project Euler
# (Problem #334)
#
# Also using this as a pretext to do some Python, very early steps!

from array import *


def display(l):
    """ 
    Displays a bean configuration list (expanded), with no spaces
    (will not work well with 2+ digit numbers of beans)

    Keyword argument:
    l -- the list containing the bean configuration
    """
    res = ""
    for x in l:
        res = "%s%d" % (res, x)
    return res


def merge(l1, l2):
    """ 
    Merges 2 (aligned) expanded bean configuration lists

    Keyword arguments:
    l1 -- first bean configuration list
    l2 -- second bean configuration list
    """
    n = len(l1)
    res = []
    for i in range(0, n):
        res.append(l1[i]+l2[i])
    return res


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
    #print display(res)
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


def beansFromList(l):
    r = array('i', l)
    return r


def decompress(l):
    res = []
    for (a, b) in l:
        for i in range(0, a):
            res.append(b)
    return res


def compress(l):
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
    x = decompress([(a, 1), (b, 2), (a, 1)])
    (l, n) = iterateAll(x)
    return n


def f3t(a, b, c):
    x = decompress([(a, 1), (b, 2), (c, 1)])
    (l, n) = iterateAll(x)
    return n


def f4t(a, b):
    return f3t(a, 1, b)


def f4(a, b):
    x = decompress([(a, 1), (1, 2), (b, 1)])
    (l, n) = iterateAll(x)
    print display(l)
    return n


def mergeBy1(config, position, count):
    n = len(config)
    a = decompress([(position-1,0),(1,1),(n-position,0)])
    l = config
    res = []
    for i in range(0, count):
        la = merge(a, l)
        (l_aux, n_aux) = iterateAll(la)
        c_aux = compress(l_aux)
        res.append((n_aux, c_aux, l_aux))
        l = l_aux
    return res
