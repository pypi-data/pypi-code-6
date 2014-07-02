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


def irrResult(values, dates, rate):
    """IRR helper function.  See irr()"""
    r = rate + 1
    result = values[0]
    for i in range(len(values)):
        result += values[i] / pow(r, (dates[i] - dates[0]) / 365)
    return result


def irrResultDeriv(values, dates, rate):
    """IRR helper function - calculates the first derivation.  See irr()"""
    r = rate + 1
    result = 0
    for i in range(len(values)):
        frac = (dates[i] - dates[0]) / 365
        result -= frac * values[i] / pow(r, frac + 1)
    return result


def irr(values, guess_rate=0.1):
    """
    IRR Calculation.  Keep consistent with $.asg.irr() in asg.coffee
    Source: https://gist.github.com/ghalimi/4597900
    """

    # Initialize dates and check that values contains at least one positive value and one negative value
    if max(values) <= 0 or min(values) >= 0:
        raise ValueError('IRR must have one positive and one negative value')

    dates = [i*365 for i in range(len(values))]
    max_epsilon = 1e-10  # Maximum epsilon for end of iteration
    max_iterations = 50  # Maximum number of iterations

    # Implement Newton's method
    count_loop = True
    iteration = 0
    while iteration < max_iterations and count_loop:
        result_value = irrResult(values, dates, guess_rate)
        new_rate = guess_rate - result_value / irrResultDeriv(values, dates, guess_rate)
        rate_delta = abs(new_rate - guess_rate)
        guess_rate = new_rate
        count_loop = (rate_delta > max_epsilon) and (abs(result_value) > max_epsilon)
        iteration += 1

    if count_loop:
        raise ValueError('Unable to find valid IRR result.')

    return guess_rate  # Return internal rate of return

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
