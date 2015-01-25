def genRec(k, B, done, w, seen, nbSeen, depth):
    """
    Parameters:
    * k is length (in bits) of the subsequences
    * B is 2 ** k (cached)
    * done is the array of cycles seen so far
    * w is the prefix being currently generated
    * seen[k] is true iff k has been seen as a subword of w
    * nbSeen = #seen
    
    Note that w has been checked already, so we're reading to extend the word...
    """
    if B == nbSeen + k - 1:
        # We're at the end, we need to check whether the k-1 words
        # that 'cross' are ok. We use the fact that the prefix is
        # always 0^k:
        ok = True
        j = 0
        wc = w
        while ok and j < k-1:
            wc = (2 * wc) % B
            ok = not seen[wc]
            j += 1
        if ok:
            done.append(w)
        return done
    else:
        # we need to check whether adding 0 or 1 works:
        w0 = (2 * w) % B
        if not seen[w0]:
            seen0 = list(seen)
            seen0[w0] = True
            done = genRec(k, B, done, 2 * w, seen0, nbSeen + 1, depth + 1)
        w1 = w0 + 1
        if not seen[w1]:
            seen1 = list(seen)
            seen1[w1] = True
            done = genRec(k, B, done, 2 * w + 1, seen1, nbSeen + 1, depth + 1)
        return done

def solve():
    # Trying some pretty naive DP:
    k = 5
    B = 2 ** k
    seen = [False for j in range(0, B)]
    seen[0] = True
    l = genRec(k, B, [], 0, seen, 1, 0)
    return sum(l)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
