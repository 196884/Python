def solve():
    # Classic sieving:
    # pInfo[n] = (p, k, p^k) where:
    # * p is the largest prime factor of n
    # * p^k is the largest power of n dividing n
    b = 10**6
    pInfo = [ (1, 1, 1) for i in range(0, b+1) ]
    sumDivs = [ 0 for i in range(0, b+1) ]
    sumDivs[1] = 1
    for n in range(2, b+1):
        (p, k, pk) = pInfo[n]
        if p == 1:
            # n is prime
            p = n
            pk = p
            k = 1
            while pk <= b:
                pkm = pk
                while pkm <= b:
                    pInfo[pkm] = (p, k, pk)
                    pkm += pk
                pk *= p
                k += 1
            sumDivs[n] = p + 1
        else:
            sumDivs[n] = ( sumDivs[n / pk] * (pk * p - 1) ) / (p - 1)

    bestLength = 0
    r = 0
    seen = [ None for i in range(0, b+1) ]
    for n in range(2, b+1):
        if seen[n] == None:
            currN = n
            seen[n] = (n, 0)
            currLength = 0
            currN = sumDivs[n] - n
            while currN <= b and seen[currN] == None:
                currLength += 1
                seen[currN] = (n, currLength)
                currN = sumDivs[currN] - currN
            if currN <= b:
                (start, prevLength) = seen[currN]
                if start == n:
                    length = currLength + 1 - prevLength
                    if length > bestLength:
                        bestLength = length
                        r = currN
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
