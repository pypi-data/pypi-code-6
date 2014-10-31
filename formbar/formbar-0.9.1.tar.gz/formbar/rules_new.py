import operator
from datetime import date
from pyparsing import (
    Forward,
    Suppress,
    Group,
    oneOf,
    ZeroOrMore,
    Word,
    Literal,
    Optional,
    Combine,
    alphas,
    nums,
    alphanums,
    operatorPrecedence,
    opAssoc
)
########################################################################
#                           Helper functions                           #
########################################################################

opmap = {
    "eq": "==",
    "ne": "!=",
    "gt": ">",
    "ge": ">=",
    "le": "<=",
    "lt": "<",
    "plus": "+",
    "minus": "-",
    "mul": "*",
    "div": "/"
}

def convertOperator(op):
    """Returns operater for a given string. Operators can be expressed
    as string known from the shell as "<" can not be included in XML"""
    op = op[0]
    return opmap.get(op, op)

def _date(p):
    p = p.strip("'")
    if p == "today":
        return date.today()
    else:
        y = int(p[0:4])
        m = int(p[4:6])
        d = int(p[6:8])
        return date(y, m, d)


def _in(a, b):
    l = []
    if isinstance(b, basestring):
        b = b.replace("'", "").replace("[", "").replace("]", "")
        for e in b.split(","):
            try:
                e = float(e)
            except:
                e = e
            l.append(e)
    else:
        l = b
    return a in l

########################################################################
#                            BNF Definition                            #
########################################################################

class Rule(object):
    def __init__(self, expr, msg=None, mode='post', triggers='error'):
        self.expr = expr
        self.expr_str = " ".join([str(t) for t in expr])
        self.msg = msg
        if msg is None:
            self.msg = 'Expression "%s" failed' % self.expr_str
        self.mode = mode
        if mode is None:
            self.mode = 'post'
        self.triggers = triggers
        if triggers is None:
            self.triggers = 'error'
        self.operators = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.div,
            ">": operator.gt,
            "<": operator.lt,
            "<=": operator.le,
            ">=": operator.ge,
            "==": operator.eq,
            "!=": operator.ne,
            "and": operator.and_,
            "or": operator.or_,
            "not": operator.not_,
            "in": _in
        }
        self.functions = {
            "date": _date,
            "bool": bool,
            "len": len
        }

    def _evaluate(self, expr, values):
        op = expr.pop()
        if op in self.operators:
            if op == "not":
                return self.operators[op](self._evaluate(expr, values))
            op2 = self._evaluate(expr, values)
            op1 = self._evaluate(expr, values)
            if isinstance(op1, basestring):
                op1 = op1.strip("'")
            if isinstance(op2, basestring):
                op2 = op2.strip("'")
            return self.operators[op](op1,op2)
        elif op in self.functions:
            return self.functions[op](self._evaluate(expr, values))
        else:
            try:
                return int( op )
            except:
                if op.startswith("$"):
                    return values[op.strip("$")]
                elif isinstance(op, basestring):
                    return "'%s'" % op
                else:
                    return op


    def evaluate(self, values=None):
        if values is None:
            values = {}
        result = self._evaluate(self.expr, values)
        return result
        #return bool(result)

class Parser(object):
    def __init__(self):
        self.expr_stack = []
        NUMBER = Word(nums)
        STRING = Combine("'" + Word(alphanums + "_") + "'")
        VAR    = Combine("$" + Word(alphanums + "_"))
        LPAR = Literal("(").suppress()
        RPAR = Literal(")").suppress()
        TRUE = Literal("True").setParseAction(lambda x: True)
        FALSE = Literal("False").setParseAction(lambda x: False)
        NOT = Literal("not")
        FUNC = oneOf("date bool len")
        ARITHOP = oneOf("+ - * / add sub mul div").setParseAction(convertOperator)
        EQOP = oneOf("== != < > <= >= eq ne gt lt ge le").setParseAction(convertOperator)
        BOOLOP = oneOf("and or")
        INCOP = Literal("in")
        EXPR = Forward()
        LIST = Combine("[" + ZeroOrMore((NUMBER|STRING|VAR)+ZeroOrMore(","+(NUMBER|STRING|VAR))) + "]").setParseAction(self.pushFirst)
        ATOM = ((FUNC+LPAR+EXPR+RPAR|NUMBER|STRING|VAR|TRUE|FALSE).setParseAction(self.pushFirst) | Group(LPAR+EXPR+RPAR))
        EXPR << ATOM + ZeroOrMore(((ARITHOP|INCOP|EQOP|BOOLOP) + (LIST|ATOM)).setParseAction(self.pushFirst))
        TERM = EXPR | (NOT + EXPR).setParseAction(self.pushFirst)
        self.BNF = TERM

    def pushFirst(self, strg, loc, toks):
        self.expr_stack.append(toks[0])

    def parse(self, expr):
        self.expr_stack = []
        control = len(expr.split())
        tree = self.BNF.parseString(expr)
        return self.expr_stack

if __name__ == "__main__":
    values = {
        "t": 1,
        "f": 0,
        "z": 2,
        "y": "1",
        "e1m": "100",
        "e1w": "120",
        "name": "test",
        "_roles": ['projektmanager', 'user', 'admin'],
        "today": date.today(),
        "x": [1, 2, 3],
    }
    tests = [("$t", True),
             ("$f", False),
             ("True", True),
             ("False", False),
             ("$t and $f", False),
             ("not ($t and $f)", True),
             ("$f or $t and $t", True),
             ("$t or $f or $t", True),
             ("($t or $f or $t) and False", False),
             ("$t + $t == $z", True),
             ("(200 * 5 / 3) > $t", True),
             ("$t in $x", True),
             ("$f in $x", False),
             ("bool($f)", False),
             ("bool($t)", True),
             ("$t gt $f", True),
             ("$name == 'test'", True),
             ("len($x) == 3", True),
             ("date('today') != date('19770312')", True),
             ("$today < date('20700312')", True),
             ("($t in [1,2,4] and $f == 0) or ($t in [0,3,5] and $f == 1) or ($t in ['', 6])", True),
             ("($y eq '1' and $z in [1,2] ) or ( $y '3' and $z in [3,4] ) or ( $y in ['','2','4'] )", True),
             ("$e1m + $e1w", True),
             ("'projektmanager' in $_roles", True),
             ("('projektmanager_2' in $_roles) == False", True),
             ("len($name) le 5", True)
             ]

    for t, expected in tests:
        p = Parser()
        rule = Rule(p.parse(t))
        res = rule.evaluate(values)
        success = "PASS" if res == expected else "FAIL"
        print success, ":", t, "->", res, "|", rule.expr_str
