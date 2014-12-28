def rotateToMin(l):
    minOut = min([l[0], l[3], l[5], l[7], l[9]])
    if l[0] == minOut:
        return l
    if l[3] == minOut:
        return [l[3], l[2], l[4], l[5], l[6], l[7], l[8], l[9], l[1], l[0]]
    if l[5] == minOut:
        return [l[5], l[4], l[6], l[7], l[8], l[9], l[1], l[0], l[2], l[3]]
    if l[7] == minOut:
        return [l[7], l[6], l[8], l[9], l[1], l[0], l[2], l[3], l[4], l[5]]
    return [l[9], l[8], l[1], l[0], l[2], l[3], l[4], l[5], l[6], l[7]]

def getKey(l):
    l = rotateToMin(l)
    a = [0, 1, 2, 3, 2, 4, 5, 4, 6, 7, 6, 8, 9, 8, 1]
    r = [str(l[a[i]]) for i in range(0, 15)]
    return int("".join(r))

def solve():
    rl = []
    numbers = [i+1 for i in range(0, 10)]
    s = set(numbers)
    for n1 in s:
        # The outermost one... because we can simply apply the rotation at the end,
        # we only look for solutions with n1 <= 6
        if n1 <= 6:
            s.remove(n1)
            for n2 in s:
                if n2 != 10:
                    s.remove(n2)
                    for n3 in s:
                        if n3 != 10:
                            total = n1 + n2 + n3 # could early abort here if too small or too high
                            s.remove(n3)
                            for n4 in s:
                                s.remove(n4)
                                n5 = total - n3 - n4
                                if n5 in s and n5 != 10:
                                    s.remove(n5)
                                    for n6 in s:
                                        s.remove(n6)
                                        n7 = total - n5 - n6
                                        if n7 in s and n7 != 10:
                                            s.remove(n7)
                                            for n8 in s:
                                                s.remove(n8)
                                                n9 = total - n7 - n8
                                                if n9 in s and n9 != 10:
                                                    s.remove(n9)
                                                    n10 = total - n2 - n9
                                                    if n10 in s:
                                                        rl.append(getKey([n1, n2, n3, n4, n5, n6, n7, n8, n9, n10]))
                                                    s.add(n9)
                                                s.add(n8)
                                            s.add(n7)
                                        s.add(n6)
                                    s.add(n5)
                                s.add(n4)
                            s.add(n3)
                    s.add(n2)
            s.add(n1)
    return max(rl)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
