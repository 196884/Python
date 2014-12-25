import math as m

def solve():
    # since 10^n has n+1 digits, all solutions are of the form d^n, with d < 10
    # if we fix d, d^n has n digits if d^n >= 10^{n-1},
    # that is n <= floor( log(10) / (log(10) - log(d)) )
    r = 0
    for d in range(1, 10):
        r += m.floor(m.log(10.0) / (m.log(10.0) - m.log(float(d))))
    return r

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
