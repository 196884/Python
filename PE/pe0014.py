def solve():
    # We store:
    # chainLength: the lengths of chains (up to current n)
    # seen: a map; if seen[k] = (a, b), it means that k was the b-th element of the sequence starting at a
    chainLength = [0]
    seen = dict()
    result = 0
    maxLength = 0
    for k in range(1, 1000000):
        done = False
        curr = k
        nb   = 0
        while not done:
            if curr == 1:
                chainLength.append(nb)
                if nb > maxLength:
                    maxLength = nb
                    result = k
                done = True
            else:
                (a, b) = seen.get(curr, (-1, -1))
                if b >= 0:
                    newNb = nb + chainLength[a] - b
                    chainLength.append(newNb)
                    if newNb > maxLength:
                        maxLength = newNb
                        result = k
                    done = True
                else:
                    seen[curr] = (k, nb)
                    if curr % 2 == 0:
                        curr /= 2
                    else:
                        curr = 3 * curr + 1
                    nb += 1
    return result

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
