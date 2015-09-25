import math

def iter(x):
    a = 2.0 ** (30.403243784 - x * x)
    f = math.floor(a)
    return f * 0.000000001

def solve():
    # it becomes stationary...
    u = -1
    for i in range(0, 600):
        f = iter(u)
        u = f
    return u + iter(u)
    
if __name__ == "__main__":
    result = solve()
    print result
