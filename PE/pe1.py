def sumOfMultiples(m, b):
    """
    Returns the sum of the multiples of m less than b
    """
    u = ( b - 1 ) / m
    result = m * u * ( u + 1 ) / 2
    return result

def solve():
    result = sumOfMultiples(3, 1000) + sumOfMultiples(5, 1000) - sumOfMultiples(15, 1000)
    print "Result: %d" % result

if __name__ == "__main__":
    solve()
