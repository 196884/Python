class node:
    def __init__(self):
        self.v = None
        self.n = None

class LL:
    def __init__(self):
        self.head = None

    def printL(self):
        n = self.head
        l = []
        while n:
            l.append(n.v)
            n = n.n
        print l

def tail(l):
    n = l.head
    while n.n:
        n = n.n
    return n.v

def llToList(l):
    r = []
    n = l.head
    while n.n:
        r.append(n.v)
        n = n.n
    r.append(n.v)
    return r

def update(n, l):
    c = l.head
    if n % c.v == 0:
        l.head = c.n
        return update(n, l)
    while c and c.n:
        if n % c.n.v == 0:
            c.n = c.n.n
        c = c.n
    return l

def solve():
    B = 1010
    # We create a linked list...
    ll = LL()
    for k in reversed(range(1, B+1)):
        v = 2 * k + 1
        nn = node()
        nn.v = v
        nn.n = ll.head
        ll.head = nn
    ll.printL()
    a = 1
    b = 1
    c = 1
    # Didn't prove anything, but found 2009 after filtering until quite far...
    # Also, it would be faster at that point to just use an array, given the little updates
    for n in range(0, 50000):
        if n % 100 == 0:
            print n
            ll.printL()
        x = a + b + c
        ll = update(x, ll)
        a = b
        b = c
        c = x
    l = llToList(ll)
    if len(l) == 124:
        return l[-1]
    return 0

if __name__ == "__main__":
    result = solve()
    print "Result: %d" % result
