import abc
import ast

import meta










# Computation decorator.
from __init__ import createUuid, Result


def scaledcomputation(*args):
    return args[0]


# Actual computation classes.
@scaledcomputation
def a():
    return 1


@scaledcomputation
def b():
    return 2

@scaledcomputation
def sum_a_b():
    return  str(5) + a() + b()

def c():
    return 3

def callcomputation(func):
    print "Calling computation: %s" % repr(func)
    return func()  # Just call the function.


def get_path_from_code(_):
    return __file__


def get_text_from_file(path):
    return open(path).read()


def get_asf_from_text(text):
    return ast.parse(text)


def get_code_from_ast(_ast):
    return compile(_ast, '<nofile>', 'exec')


def get_ast_for_func(func):
    return meta.decompile(func)


def get_code_for_ast(func):
    return meta.dump_python_source(func)


def find_decorated_functions(node):
    decorated_functions = []
    for x in ast.walk(node):
        assert isinstance(x, ast.AST)
        if isinstance(x, ast.FunctionDef):
            assert isinstance(x, ast.FunctionDef)
            for y in x.decorator_list:
                assert isinstance(y, ast.Name)
                print "decorator: %s %s" % (y.id, y.ctx)
                assert isinstance(y.ctx, ast.Load)
                print "  load: %s" % y.ctx
                if True:  # Find our decorator.
                    decorated_functions.append(x)
    return decorated_functions


def modelcomputation(func):
    path = get_path_from_code(func)
    print "Path: %s" % path
    text = get_text_from_file(path)
    print "Text: %s" % text.split('\n')[0]
    ast_node = get_asf_from_text(text)
    print "Ast: %s" % ast_node
    code = get_code_from_ast(ast_node)
    print "Code: %s" % code
    decorated_functions = find_decorated_functions(ast_node)
    print "Decorated functions: %s" % " ".join(f.name for f in decorated_functions)


def main():
    print "Computation result: %s" % sum_a_b()
    print "Call computation result: %s" % callcomputation(sum_a_b)
    print "Model computation: %s" % modelcomputation(sum_a_b)


# Domain.

# Domain services.



def createModelledFunction(modified_func_def):
    modelled_function_id = createUuid()
    obj = ModelledFunction(id=modelled_function_id,
                           stubbedExpr=modified_func_def)
    registry.functions[obj.id] = obj
    return obj








# Domain objects.

# Todo: Introduce reflective registry and objects with meta attributes.

class ModelledFunction(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, id, stubbedExpr):
        self.id = id
        self.stubbedExpr = stubbedExpr

    def evaluate(self, resultsRegister, stubIds, **kwds):
        import __init__
        stubbedExpr = self.stubbedExpr
        assert isinstance(stubbedExpr, __init__.DslExpression)
        dslNamespace = __init__.DslNamespace()
        for stubId in stubIds:
            stubResult = resultsRegister[stubId]
            assert isinstance(stubResult, Result)
            dslNamespace[stubId] = stubResult.value
        simpleExpr = stubbedExpr.reduce(dslLocals=dslNamespace, dslGlobals={})
        return simpleExpr.evaluate(**kwds)


# Utilities.

def dump(node, annotate_fields=True, include_attributes=False, indent='  '):
    """
    Return a formatted dump of the tree in *node*.  This is mainly useful for
    debugging purposes.  The returned string will show the names and the values
    for fields.  This makes the code impossible to evaluate, so if evaluation is
    wanted *annotate_fields* must be set to False.  Attributes such as line
    numbers and column offsets are not dumped by default.  If this is wanted,
    *include_attributes* can be set to True.
    """
    def _format(node, level=0):
        if isinstance(node, ast.AST):
            fields = [(a, _format(b, level)) for a, b in ast.iter_fields(node)]
            if include_attributes and node._attributes:
                fields.extend([(a, _format(getattr(node, a), level))
                               for a in node._attributes])
            return ''.join([
                node.__class__.__name__,
                '(',
                ', '.join(('%s=%s' % field for field in fields)
                           if annotate_fields else
                           (b for a, b in fields)),
                ')'])
        elif isinstance(node, list):
            lines = ['[']
            lines.extend((indent * (level + 2) + _format(x, level + 2) + ','
                         for x in node))
            if len(lines) > 1:
                lines.append(indent * (level + 1) + ']')
            else:
                lines[-1] += ']'
            return '\n'.join(lines)
        return repr(node)

    if not isinstance(node, ast.AST):
        raise TypeError('expected AST, got %r' % node.__class__.__name__)
    return _format(node)