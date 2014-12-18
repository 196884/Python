# Simple polynomial manipulation functions

from array import *


def eval(p, x):
    """
    Given a polynomial encoded as an array of coefficients,
    evaluate it at a specified point

    Keyword argument:
    p -- the list of polynomial coefficients
    x -- the value at which to evaluate
    """
    n = len(p)
    r = 0
    for i in range(0, n):
        r += x * r + p[n-1-i]
    return r


def binomials(n):
    """
    Computes all binomial coefficients up to level n

    Returns a list of lists C such that C[n][k] = n choose k

    Keyword argument:
    n -- level up to which to compute
    """
    result = []
    prev = []
    while len(result) <= n:
        x = 0
        l = []
        for y in prev:
            l.append(x+y)
            x = y
        l.append(1)
        result.append(l)
        prev = l
    return result


def evalList(p, n, offset = 0):
    result = []
    for k in range(0, n):
        result.append(eval(p, offset + k))
    return result


def reconstructOneStep(l, C):
    """
    Helper function for polynomial reconstruction

    Given P(X+1)-P(X), computes P (assuming P(0) = 0)

    Keyword arguments:
    l -- the coefficients of P(X+1)-P(X)
    C -- precomputed binomial coefficients (up to the degree)
    """
    n = len(l)
    curr = l
    result = []
    for k in range(0, n):
        coef = curr[n-1-k] / (n-k)
        result.append(coef)
        for i in range(0, n-k):
            curr[i] -= C[n-k][i] * coef
    result.append(0)
    return result[::-1]


def reconstruct(l, offset=0):
    """
    Given an array l corresponding to values taken by an (unknown)
    polynomial P, reconstructs the polynomial.

    Returns an array of the form [p_0, p_1,..., p_k]
    encoding P(X) = \sum _i p_i X^i

    P is assumed to be of degree < len(l)

    Keyword argument:
    l      -- the values taken by P on successive integers (starting at offset)
    offset -- the integer such that l[0] == P(offset)
    """
    n = len(l)
    # We start by taking all finite differences (up to the point where they're zero)
    diffs = [l]
    prevDiff = l
    degree   = 0
    for i in range(1, n):
        diff = []
        for j in range(0, n-i):
            diff.append(prevDiff[j+1] - prevDiff[j])
        diffs.append(diff)
        prevDiff = diff
        if len(set(diff)) > 1 or diff[0] != 0:
            degree += 1
    # We precompute all the needed binomial coefficients:
    C = binomials(degree)
    result = [diffs[degree][0]]
    for k in reversed(range(1, degree+1)):
        result = reconstructOneStep(result, C)
        result[0] += diffs[k-1][0] - eval(result, offset) 
    return result
    
            

