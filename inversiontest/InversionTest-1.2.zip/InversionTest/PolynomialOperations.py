"""
Basic univariate polynomial multiplication and division
Polynomials are represented as sequences of coefficients,
where the highest coefficient of an expression is stored
at index=0.  So then, [1, 5, 3] = (x^2 + 5x + 3).

This implementation of expansion (multiplication) is
more robust than its division counterpart.  While
expansion should work for any set of expressions,
the division will only work for monic polynomials.

Author: Benjamin D. Nye
License: Apache License V2.0
"""

def polynomialExpansion(*coefficients):
    """
    Expand lists of coefficients for univariate polynomials
    into a single list of coefficients for the expanded polynomial
    @param coefficients: Lists of integer coefficients
    @type coefficients: list of list of int
    @return: Single list of coefficients for the expanded polynomial
    @rtype: list of int
    """
    if len(coefficients) == 0 or any(len(coeffs)==0 for coeffs in coefficients):
        return []
    expanded = coefficients[0][:]
    for coeffs in coefficients[1:]:
        # Expand to fit new higher-order terms
        numCoeff = len(coeffs)
        expanded.extend([0]*(numCoeff-1))
        # Multiply and collect
        for i in xrange(len(expanded)-1,-1,-1):
            expanded[i] = sum([expanded[i-j]*coeff for j, coeff in enumerate(coeffs[:i+1])])
    return expanded
        
def syntheticDivision(numerator, divisor):
    """
    Perform a polynomial division using syntethic division
    Returns the new coefficients in two parts: quotient and remainder
    WARNING: Only works for monic polynomials
    @param numerator: Coefficients for the numerator
    @type numerator: list of int
    @param divisor: Coefficients of the divisor
    @type divisor: list of int
    @return: Quotient (whole part) and remainder of division.  Note: remainder contains only the numberator part
    @rtype: tuple of (list of int, list of int)
    """
    numerator = removeEmptyTerms(numerator)
    divisor = removeEmptyTerms(divisor)
    numeratorLen = len(numerator)
    divisorLen = len(divisor)
    if (divisorLen > numeratorLen or len(numerator) == 0 or
        (divisorLen==numeratorLen and divisor > numerator)):
        return [], numerator
    elif divisorLen == 0:
        return numerator, []
    value = numerator[0]
    quotient = [value]
    for i in xrange(1, numeratorLen):
        colStart = max(1, i-(numeratorLen-divisorLen))
        colEnd = min(i+1, divisorLen)
        columnVal = sum([-quotient[i-j]*divisor[j] for j in xrange(colStart, colEnd)])
        quotient.append(numerator[i] + columnVal)
    if divisorLen == 1:
        return quotient, []
    else:
        return quotient[:-divisorLen+1], quotient[-divisorLen+1:]

def removeEmptyTerms(series, removeFromHead=True):
    """
    Remove leading (head) or trailing (tail) zeros
    from an expression.  This is needed to properly
    evaluate the actual terms in the expression.
    @param series: Series of coefficients
    @type series: list of int or float
    @param removeFromHead: If True, remove zeroes from start of series; else, remove from tail.
    @type removeFromHead: bool
    @return: Series with zero-padding removed
    @rtype: list of int or float
    """
    if removeFromHead:
        i=0
        for i, x in enumerate(series):
            if x != 0:
                break
        if i != 0:
            series = series[i:]
    else:
        i=len(series)
        for i in xrange(len(series)-1,-1,-1):
            if series[i] != 0:
                break
        if i != 0:
            series = series[:i+1]
    return series
            
