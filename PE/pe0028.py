# Closed form...

def solve():
    k = 500 
    r = 3 * k + (2*k+1)*(2*k+2)*(4*k+3)/6+8*k*(k+1)*(2*k+1)/6
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
