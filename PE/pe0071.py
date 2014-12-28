def solve():
    # We simply walk down the Stern-Brocot tree (we know the answer is in between 2/5 and 3/7)
    # the elements are going to be of the form:
    # (2 + 3k) / (5 + 7k)
    # and we want 5 + 7k <= 1000000, i.e.,
    result = 2 + 3 * ((1000000 - 5) / 7)
    return result

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
