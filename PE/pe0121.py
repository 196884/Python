def solve():
    n = 15 
    k = 1
    l = [1]
    while k <= n:
        lNew = [1]
        for j in range(1, k):
            lNew.append(k * l[j-1] + l[j])
        lNew.append(k * l[-1])
        l = lNew
        k += 1
    d = sum(l)
    n = sum(l[0:(n+1)/2])
    return d / n

if __name__ == "__main__":
    result = solve()
    print "Result: %s" % result
