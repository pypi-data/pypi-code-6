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

from constants import Symbol, R_EXP, R_MOD, R_DIV, R_MUL, R_ADD, R_SUB, M_PI, M_E, FUNCTION_MAP, OPERATOR_MAP


class MathJS(object):
    """
    Derived from Paul McGuire's work on fourFn.py and lispy.html
    http://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string
    http://pyparsing.wikispaces.com/file/view/fourFn.py
    http://pyparsing.wikispaces.com/message/view/home/15549426
    http://norvig.com/lispy.html

    Usage:

    mjs = MathJS()
    input_data = {'var_a': 5}
    mjs.update(input_data)    # Sets variables used in equations
    mjs.eval('var_a + 5 * 2')

    MathJS.eval() is the main calculating function.  It will change operators to functions, parse and then evaluate.

    MathJS.eval_map() evaluates an expressions list, recursively storing the results as re-usable variables
    MathJS.eval_map([['var_a', '5 + 2'], ['var_b', 'var_a + 3']])
    """
    def __init__(self):
        self.data = {'pi': M_PI, 'e': M_E}
        self.fn = FUNCTION_MAP
        self.operator = OPERATOR_MAP

    @staticmethod
    def atom(token):
        """Numbers become numbers; every other token is a symbol (string)."""
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return Symbol(token)

    @staticmethod
    def isNumber(value):
        """Evaluates if atom is a number - TODO - check isNumber(True) is a number, int(True) = 1"""
        try:
            _ = 0 + value
            return True
        except TypeError:
            return False

    @staticmethod
    def tokenize(s):
        """Convert a string expression into a series of tokens"""
        return ['('] + s.replace('[', '(').replace(']', ')').replace('(', ' ( ').replace(')', ' ) ')\
            .replace(',', ' , ').split() + [')']

    def eval(self, expression):
        """
        Main MathJS function - it breaks down an expression into tokens, converts */+- into functions which
        preserve the order of operations, and then evaluates the resulting parsed tokens.
        """
        tokens = self.tokenize(expression)
        clean_expression = self.operator_formatter(tokens)[0]
        tokens = self.tokenize(clean_expression)
        parsed_tokens = self.parse(tokens)
        return self.eval_parsed_tokens(parsed_tokens)

    def eval_map(self, expression_map):
        """
        An Expression map is a tuple of the form ('variable name', 'expression') where the result
        of the expression will be stored in the data dictionary, and accessible to subsequent
        expressions.
        """
        for row in expression_map:
            self.data[row[0]] = self.eval(row[1])

    def eval_parsed_tokens(self, parsed_tokens):
        """Evaluate an expression of parsed_tokens."""
        multiple_values = []
        value = 0
        current_fn = None
        current_operator = None
        for i, v in enumerate(parsed_tokens):
            if v == ',':
                multiple_values.append(value)
                value = 0
            elif isinstance(v, list):
                # Lists are used to hold values for functions
                parsed_tokens[i] = self.eval_parsed_tokens(v)
                if current_fn:
                    # Evaluate current function
                    if isinstance(parsed_tokens[i], tuple):
                        value = self.fn[current_fn](*parsed_tokens[i])
                    else:
                        value = self.fn[current_fn](parsed_tokens[i])
                    current_fn = None
                else:
                    if isinstance(parsed_tokens[i], tuple):
                        # Allow tuple as potential function argument
                        value = parsed_tokens[i]
                    else:
                        value = parsed_tokens[i]
            elif isinstance(v, Symbol):
                if v in self.fn:
                    current_fn = v
                    continue  # Proceed to next token
                elif v in self.operator:
                    if i == 0:
                        if v in ('+', '-'):
                            current_operator = (v, 0)  # eg '-5 + 3' is '0 - 5
                        else:
                            raise AttributeError('Invalid first operator: {0} for {1}'.format(v, parsed_tokens))
                    else:
                        current_operator = (v, parsed_tokens[i-1])
                else:
                    raise AttributeError('Unknown Symbol: {0} in {1}'.format(v, parsed_tokens))
            else:
                # Should be a numerical value!
                if current_operator:
                    value = self.operator[current_operator[0]](current_operator[1], v)
                    current_operator = None
                else:
                    value = v

        if len(multiple_values):
            # Return list (ie, parameters for function)
            multiple_values.append(value)
            return tuple(multiple_values)
        else:
            # Return single value
            return value

    def operator_formatter(self, tokens, loop=0):
        """
        Change operators ^, %, /, *, +, - into functions, preserving the order of operations.
        """
        i = 0
        current = []
        while i < len(tokens):
            if tokens[i] == '(':
                current.append('(')
                fixed_string, increment = self.operator_formatter(tokens[i+1:], loop+1)
                current.append(fixed_string)
                i += increment + 1
            elif tokens[i] == ')':
                fixed_string = self.operators_to_ordered_functions(' '.join(current))
                return fixed_string+' )', i + 1
            elif tokens[i] == ',':
                # Treat comma like )(
                fixed_string = self.operators_to_ordered_functions(' '.join(current))
                fixed_string_after_comma, increment = self.operator_formatter(tokens[i+1:], loop+1)
                return '{0}, {1}'.format(fixed_string, fixed_string_after_comma), i + increment + 1
            else:
                current.append(tokens[i])
                i += 1
        return ' '.join(current), i

    @staticmethod
    def operator_converter_factory(func_name):
        """
        Returns a function that returns a string expression that would a list to the given func_name
        """
        def _process(matchobj):
            args = map(str.strip, matchobj.groups())
            if not all(args):
                raise SyntaxError('Invalid syntax.')
            args = map(MathJS.operators_to_ordered_functions, args)
            return '{0}({1})'.format(func_name, ', '.join(args))

        return _process

    @staticmethod
    def operators_to_ordered_functions(expr):
        """
        Processes an expression, replacing relevant parts with their equivalent functions.  Maintains correct
        order of operations.
        http://sunjay.ca/2014/04/27/evaluating-simple-math-expressions-using-python-and-regular-expressions/
        """
        # expr = R_PAR.sub(lambda m: MathJS.operators_to_ordered_functions(m.group(1)), expr)
        expr = R_EXP.sub(MathJS.operator_converter_factory("pow"), expr)
        expr = R_MOD.sub(MathJS.operator_converter_factory("mod"), expr)
        expr = R_DIV.sub(MathJS.operator_converter_factory("div"), expr)
        expr = R_MUL.sub(MathJS.operator_converter_factory("mul"), expr)
        expr = R_ADD.sub(MathJS.operator_converter_factory("add"), expr)
        expr = R_SUB.sub(MathJS.operator_converter_factory("sub"), expr)
        return expr

    def parse(self, tokens):
        """Parse an expression from a sequence of tokens."""
        if len(tokens) == 0:
            raise SyntaxError('Unexpected EOF while reading')
        token = tokens.pop(0)
        if '(' == token:
            L = []
            while tokens[0] != ')':
                L.append(self.parse(tokens))
            tokens.pop(0)  # pop off ')'
            return L
        elif ')' == token:
            raise SyntaxError('unexpected )')
        else:
            atom = self.atom(token)
            if atom in self.data and self.isNumber(self.data[atom]):
                return self.data[atom]
            else:
                return atom

    def get(self, key):
        """Get a value from the data dictionary."""
        if key in self.data:
            return self.data[key]
        else:
            return None

    def set(self, key, value):
        """
        Set a value in the data dictionary.  The keys in this dictionary can be used as
        and updated by the evaluation of the expression. For example:
        mjs.data = {'var_a': 3}
        mjs.eval('var_a + 7')   # returns 10
        """
        self.data[key] = value

    def update(self, data):
        """Update the local data dictionary with variables to be used by the calculations"""
        self.data.update(data)
