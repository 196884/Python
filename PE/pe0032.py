# Looking for 'pandigital products':
# x * y = z
# with the concatenation of x, y and z pandigital
# 
# We assume x < y, and let
# x \in [10^a, 10^{a+1}[
# y \in [10^b, 10^{b+1}[
# z \in [10^c, 10^{c+1}[
#
# pandigital => a+b+c=6
# product => c = a+b or c = a+b+1
# so that
# a+b=3
# the only 2 possible cases are
# * a=0, b=3
# * a=1, b=2

def testFactors(x,y):
    z = x * y
    factors = []
    while x > 0:
        factors.append(x%10)
        x /= 10
    while y > 0:
        factors.append(y%10)
        y /= 10
    while z > 0:
        factors.append(z%10)
        z /= 10
    factors.sort()
    return factors == [1,2,3,4,5,6,7,8,9]

def solve():
    pSet = set()
    for x in range(1, 10):
        for y in range(1000, 10000):
            if testFactors(x, y):
                pSet.add(x * y)
    for x in range(10, 100):
        for y in range(100, 1000):
            if testFactors(x, y):
                pSet.add(x * y)
    l = list(pSet)
    return sum(l)

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result

