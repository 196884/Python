import random as rand
from operator import itemgetter

squares = [
    "GO",
    "A1",
    "CC1",
    "A2",
    "T1",
    "R1",
    "B1",
    "CH1",
    "B2",
    "B3",
    "JAIL",
    "C1",
    "U1",
    "C2",
    "C3",
    "R2",
    "D1",
    "CC2",
    "D2",
    "D3",
    "FP",
    "E1",
    "CH2",
    "E2",
    "E3",
    "R3",
    "F1",
    "F2",
    "U2",
    "F3",
    "G2J",
    "G1",
    "G2",
    "CC3",
    "G3",
    "R4",
    "CH3",
    "H1",
    "T2",
    "H2"
]

def solve():
    # MC, for convenience (can also look at the Markov chain transition matrix...)
    invSquares = dict()
    nbSquares = len(squares)
    for i in range(0, nbSquares):
        invSquares[squares[i]] = i
    cc1  = invSquares["CC1"]
    cc2  = invSquares["CC2"]
    cc3  = invSquares["CC3"]
    ch1  = invSquares["CH1"]
    ch2  = invSquares["CH2"]
    ch3  = invSquares["CH3"]
    g2j  = invSquares["G2J"]
    go   = invSquares["GO"]
    jail = invSquares["JAIL"]
    c1   = invSquares["C1"]
    e3   = invSquares["E3"]
    h2   = invSquares["H2"]
    r1   = invSquares["R1"]
    r2   = invSquares["R2"]
    r3   = invSquares["R3"]
    r4   = invSquares["R4"]
    u1   = invSquares["U1"]
    u2   = invSquares["U2"]
    chToR = { ch1: r2, ch2: r3, ch3: r1 }
    chToU = { ch1: u1, ch2: u2, ch3: u1 }

    nbVisits = [0 for i in range(0, nbSquares)]
    N = 1000000
    curr = go
    for n in range(0, N):
        dice1 = rand.randrange(1, 5)
        dice2 = rand.randrange(1, 5)
        dices = dice1 + dice2
        curr = (curr + dices) % nbSquares
        if curr == cc1 or curr == cc2 or curr == cc3:
            rnd = rand.randrange(0, 16)
            if rnd == 0:
                curr = go
            elif rnd == 1:
                curr = jail
        elif curr == ch1 or curr == ch2 or curr == ch3:
            rnd = rand.randrange(0, 16)
            if rnd == 0:
                curr = go
            elif rnd == 1:
                curr = jail
            elif rnd == 2:
                curr = c1
            elif rnd == 3:
                curr = e3
            elif rnd == 4:
                curr = h2
            elif rnd == 5:
                curr = r1
            elif rnd == 6 or rnd == 7:
                curr = chToR[curr]
            elif rnd == 8:
                curr = chToU[curr]
            elif rnd == 9:
                curr = (curr - 3) % nbSquares
        elif curr == g2j:
            curr = jail
        nbVisits[curr] += 1

    totals = []
    for i in range(0, nbSquares):
        totals.append((i, nbVisits[i]))
    totals.sort(key=itemgetter(1), reverse = True)
    r = ""
    for k in range(0, 3):
        (d, _) = totals[k]
        if d < 10:
            r = "%s0" % r
        r = "%s%d" % (r, d)
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %s" % result
