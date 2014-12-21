def isLeapYear(y):
    if y % 4 != 0:
        return False
    if y % 400 == 0:
        return True
    if y % 100:
        return False
    return True

months = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]

def incDate(d, m, y):
    if d >= months[ m ]:
        # except if leap year, we flip to the next month
        if m == 11:
            return (1, 0, y+1)
        if m == 1 and isLeapYear(y) and d == 28:
            return (d+1, m, y)
        return (1, m+1, y)
    return (d+1, m, y)

def solve():
    day = 0 # Monday
    d = 1
    m = 0
    y = 1900
    result = 0
    while y < 2001:
        if y >= 1901 and day == 6 and d == 1:
            result += 1
        (d, m, y) = incDate(d, m, y)
        day = (day + 1) % 7
    return result

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
