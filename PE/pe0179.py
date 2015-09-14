import array

def solve():
    n = 10**7
    r = 0
    powers = array.array('i', (1 for i in range(0, n+1)))
    ppowa  = array.array('i', (1 for i in range(0, n+1)))
    nfa   = [ 0, 1 ]
    nfl   = 1 # the last element of nfa
    for k in range(2, n+1):
        if ppowa[k] == 1:
            # Case where k is prime
            if nfl == 2:
                r += 1
            nfl = 2
            nfa.append(nfl)
            p = k
            ppow = p
            power = 1
            while ppow <= n:
                ppowMul = ppow
                while ppowMul <= n:
                    powers[ ppowMul ] = power
                    ppowa[ ppowMul ] = ppow
                    ppowMul += ppow
                ppow *= p
                power += 1
        else:
            # k is not prime
            aux = nfa[ k / ppowa[k] ] * (1 + powers[k])
            if aux == nfl:
                r += 1
            nfl = aux
            nfa.append(nfl)
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
