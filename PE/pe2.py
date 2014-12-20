def sumFiboEven(n):
    """
    Returns the sum of the even Fibonacci numbers that are < n

    Uses the fact that if G(n) is F(0)+...+F(n), then
    G(n) = F(n+2) - 1
    and also that:
    * the even Fibonacci numbers are the F(3*k+2)
    * the sum of the even Fibonacci numbers <= F(3*k+2) is G(3*k+2) / 2
    
    This means that to get the result, we just compute the Fibonacci numbers,
    and if F(k) is the first even one *above* n, we return F(k-1) / 2
    """
    a = 1
    b = 1
    while True:
        aux = a + b
        if aux >= n and aux % 2 == 0:
            return ( b - 1 ) / 2
        a = b
        b = aux

def solve():
    result = sumFiboEven(4000000)
    print "Result: %d" % result

if __name__ == "__main__":
    solve()
