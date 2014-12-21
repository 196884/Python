import numpy as np

def solve():
    phi = (1.0 + np.sqrt(5.0))/2
    f   = ( 999.0 * np.log(10.0) + 0.5 * np.log(5.0) ) / np.log(phi)
    return int(f) + 1

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
