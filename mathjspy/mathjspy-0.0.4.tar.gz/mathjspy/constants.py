# Copyright (c) 2014 mathjspy
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# @license: http://www.opensource.org/licenses/mit-license.php
# @author: see AUTHORS file


from re import compile
from math import pow, sqrt, pi, e, sin, cos, tan, fmod, log
from operator import add, sub, mul, truediv, not_, gt, lt, ge, le, eq
from numpy import irr

Symbol = str

# All operators: ^ % / * + -
# R_PAR = compile("\(([^)]+)\)")
R_EXP = compile("([^%/*+-]+)\^([^%/*+-]+)")
R_MOD = compile("([^/*+-]+)%([^/*+-]+)")
R_DIV = compile("([^*+-]+)\/([^*+-]+)")
R_MUL = compile("([^+-]+)\*([^+-]+)")
R_ADD = compile("([^-]+)\+([^-]+)")
R_SUB = compile("(.+)\-(.+)")

M_PI = pi
M_E = e


# Custom Functions
def ifElse(expression, ifTrue, ifFalse):
    if expression:
        return ifTrue
    else:
        return ifFalse


def npv(rate, payments):
    """ NPV calculation."""
    value = 0
    for i, payment in enumerate(payments):
        value += payment / pow((1 + rate), i)
    return value


def alt_irr(cashflows, guess_rate=1.0):
    """
    The IRR or Internal Rate of Return is the annualized effective compounded return rate which can be earned on the
    invested capital, i.e., the yield on the investment.  This formula is not always accurate.

    http://stackoverflow.com/questions/6892900/what-is-the-numerical-method-used-in-this-implementation-of-irr
    """
    iterations = 100
    investment = cashflows[0]
    for i in range(1, iterations+1):
        guess_rate *= (1 - npv(guess_rate, cashflows) / investment)
    return guess_rate


# Functions take input in the tokenized form fn(a, b, c)
FUNCTION_MAP = {
    'add': add,
    'cos': cos,
    'div': truediv,
    'ifElse': ifElse,
    'irr': irr,
    'log': log,
    'max': max,
    'min': min,
    'mod': fmod,
    'mul': mul,
    'npv': npv,
    'pow': pow,
    'round': round,
    'sgn': lambda a: abs(a) > 1e-12 and cmp(a, 0) or 0,
    'sin': sin,
    'sqrt': sqrt,
    'sub': sub,
    'tan': tan,
    'trunc': lambda a: int(a),
}

# Operators take input in the tokenized form: a op b
# Note +,-,*,/,^,% are converted to functions to preserve order of operations
OPERATOR_MAP = {
    'not': not_,
    '>': gt,
    '<': lt,
    '>=': ge,
    '<=': le,
    '=': eq,
    '==': eq,
}
