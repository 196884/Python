# Given a number of the form n = q.10^a+r, with
# q\in [1,9]
# r < 10^a
# Returns the triple (a, q, r)
def tripleFn(n):
    mul = 1
    a = 0
    r = 0
    while n > 9:
        r   += mul * ( n % 10 )
        a   += 1
        mul *= 10
        n   /= 10
    return (a, n, r)

# g(a) := f(10^a - 1, d)
def g(a):
    return a * 10 ** (a - 1)

def f(n, d):
    if n < 10:
        if n < d:
            return 0
        else:
            return 1
    (a, q, r) = tripleFn(n)
    result    = f(r, d) + q * g(a)
    if d < q:
        result += 10**a
    if d == q:
        result += r + 1
    return result

def t(n, d):
    return f(n, d)-n

def fEnum(n, d):
    a = 0
    for k in range(1, n+1):
        x = k
        while x > 0:
            if x % 10 == d:
                a += 1
            x /= 10
        c = f(k, d)
        print "%d - %d - %d" % (k, a, c)
    return a

def solve():
    r = 0

    # Done more or less manually, using dichotomy and f above
    l1 = [ 0 ]
    # for 1:
    l1.append(          1 )
    l1.append(     199981 )
    l1.append(     199982 )
    l1.append(     199983 )
    l1.append(     199984 )
    l1.append(     199985 )
    l1.append(     199986 )
    l1.append(     199987 )
    l1.append(     199988 )
    l1.append(     199989 )
    l1.append(     199990 )
    l1.append(     200000 )
    l1.append(     200001 )
    l1_a = list( l1 )
    l1.append(    1599981 )
    l1.append(    1599982 )
    l1.append(    1599983 )
    l1.append(    1599984 )
    l1.append(    1599985 )
    l1.append(    1599986 )
    l1.append(    1599987 )
    l1.append(    1599988 )
    l1.append(    1599989 )
    l1.append(    1599990 )
    l1.append(    2600000 )
    l1.append(    2600001 )
    l1.append(   13199998 )
    for x in l1_a:
        l1.append( 35000000 + x )
    l1_b = list( l1 )
    l1.append(  117463825 )
    for x in l1_b:
        l1.append( 500000000 + x )
    l1.append( 1111111110 )
    print "%d -> %d" % (1, sum( l1 ))
    r += sum( l1 )

    # for 2:
    l2 = [ 0 ]
    l2.append( 28263827 )
    l2.append( 35000000 )
    l2_2 = list(l2)
    l2.append( 242463827 )
    for x in l2_2:
        l2.append( 500000000 + x )
    l2_6 = list(l2)
    for x in l2_6:
        l2.append( 10000000000 + x )
    print "%d -> %d" % (2, sum( l2 ))
    r += sum(l2)

    # for 3
    l3 = [ 0 ]
    l3.append( 371599983 )
    l3.append( 371599984 )
    l3.append( 371599985 )
    l3.append( 371599986 )
    l3.append( 371599987 )
    l3.append( 371599988 )
    l3.append( 371599989 )
    l3.append( 371599990 )
    l3.append( 371599991 )
    l3.append( 371599992 )
    l3.append( 500000000 )
    l3_11 = list(l3)
    for k in range( 1, 3 ):
        for x in l3_11:
            l3.append( k * 10000000000 + x )
    print "%d -> %d" % (3, sum( l3 ))
    r += sum(l3)

    # for 4
    l4 = [ 0 ]
    l4.append( 499999984 )
    l4.append( 499999985 )
    l4.append( 499999986 )
    l4.append( 499999987 )
    l4.append( 499999988 )
    l4.append( 499999989 )
    l4.append( 499999990 )
    l4.append( 499999991 )
    l4.append( 499999992 )
    l4.append( 499999993 )
    l4.append( 500000000 )
    l4_11 = list( l4 )
    for k in range( 1, 4 ):
        for x in l4_11:
            l4.append( k * 10000000000 + x )
    print "%d -> %d" % (4, sum( l4 ))
    r += sum(l4)

    # for 5
    l5 = [ 0 ]
    l5.append( 10000000000 )
    l5.append( 20000000000 )
    l5.append( 30000000000 )
    l5.append( 40000000000 )
    print "%d -> %d" % (5, sum( l5 ))
    r += sum( l5 )

    # for 6
    l6 = [ 0 ]
    l6.append( 9500000000 )
    l6.append( 9628399986 )
    l6.append( 9628399987 )
    l6.append( 9628399988 )
    l6.append( 9628399989 )
    l6.append( 9628399990 )
    l6.append( 9628399991 )
    l6.append( 9628399992 )
    l6.append( 9628399993 )
    l6.append( 9628399994 )
    l6.append( 9628399995 )
    l6_2 = list( l6 )
    for k in range( 1, 6 ):
        for x in l6_2:
            l6.append( k * 10000000000 + x )
    print "%d -> %d" % (6, sum( l6 ))
    r += sum(l6)

    # for 7
    l7 = [ 0 ]
    l7.append( 9465000000 )
    l7.append( 9471736170 )
    l7.append( 9500000000 )
    l7.append( 9757536170 )
    l7.append( 9965000000 )
    l7.append( 9971736170 )
    l7_a = list( l7 )
    for k in range( 1, 7 ):
        for x in l7_a:
            l7.append( k * 10000000000 + x )
    print "%d -> %d" % (7, sum( l7 ))
    r += sum( l7 )

    # for 8
    l8 = [ 0 ]
    l8.append( 9465000000 )
    l8.append( 9486799989 )
    l8.append( 9486799990 )
    l8.append( 9486799991 )
    l8.append( 9486799992 )
    l8.append( 9486799993 )
    l8.append( 9486799994 )
    l8.append( 9486799995 )
    l8.append( 9486799996 )
    l8.append( 9486799997 )
    l8.append( 9497400000 )
    l8.append( 9498399989 )
    l8.append( 9498399990 )
    l8.append( 9498399991 )
    l8.append( 9498399992 )
    l8.append( 9498399993 )
    l8.append( 9498399994 )
    l8.append( 9498399995 )
    l8.append( 9498399996 )
    l8.append( 9498399997 )
    l8.append( 9500000000 )
    l8.append( 9882536171 )
    l8.append( 9965000000 )
    l8.append( 9986799989 )
    l8.append( 9986799990 )
    l8.append( 9986799991 )
    l8.append( 9986799992 )
    l8.append( 9986799993 )
    l8.append( 9986799994 )
    l8.append( 9986799995 )
    l8.append( 9986799996 )
    l8.append( 9986799997 )
    l8.append( 9997400000 )
    l8.append( 9998399989 )
    l8.append( 9998399990 )
    l8.append( 9998399991 )
    l8.append( 9998399992 )
    l8.append( 9998399993 )
    l8.append( 9998399994 )
    l8.append( 9998399995 )
    l8.append( 9998399996 )
    l8.append( 9998399997 )
    l8_a = list( l8 )
    for k in range( 1, 8 ):
        for x in l8_a:
            l8.append( k * 10000000000 + x )
    print "%d -> %d" % (8, sum( l8 ))
    r += sum( l8 )

    # for 9
    l9 = [ 0 ]
    l9.append( 10000000000 )
    l9.append( 20000000000 )
    l9.append( 30000000000 )
    l9.append( 40000000000 )
    l9.append( 50000000000 )
    l9.append( 60000000000 )
    l9.append( 70000000000 )
    l9.append( 80000000000 )
    print "%d -> %d" % (9, sum( l9 ))
    r += sum( l9 )
    return r

if __name__ == "__main__":
    # Really ugly, but works (don't want to spend time coding what I actually did :) )
    result = solve()
    print "Result: %d" % result


