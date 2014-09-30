# Quick, dirty way to generate wrapper functions by iterating over cffi's
# parsed declarations.

import cffi.model
import collections
import re

# get the pycparser that cffi is using
import cffi.cparser
Decl = cffi.cparser.pycparser.c_ast.Decl
FuncDecl = cffi.cparser.pycparser.c_ast.FuncDecl

from . import errorprone, nullable

def is_primitive(arg):
    """Return True if arg is primitive"""
    primitive = False
    if hasattr(arg, 'ALL_PRIMITIVE_TYPES') and arg.get_c_name() in arg.ALL_PRIMITIVE_TYPES:
        primitive = True
    return primitive

def is_direct(arg):
    """Return True if arg can be handled directly by cffi."""
    return (is_primitive(arg) or
            (getattr(arg, 'kind', '') == 'enum'))

def is_utf8(arg):
    """
    Return True if arg should be utf8.

    TODO figure out which char* are not utf8.
    """
    if (arg.get_c_name() in ('char *', 'char const *')):
        return True
    return False

def is_primitive_or_primitive_p(arg):
    """Return True if arg is primitive or primitive*"""
    primitive = False
    if hasattr(arg, 'totype'):
        arg = arg.totype  # a pointer
    primitive = is_primitive(arg)
    return primitive

def is_primitive_p(arg):
    """Return True if arg is primitive*"""
    return is_primitive_or_primitive_p(arg) and hasattr(arg, 'totype')

class IndentedWriter(object):
    def __init__(self, writer):
        self.writer = writer
        self.level = 0
        self.indentation = "    "

    def writeln(self, msg):
        self.writer.write(self.indentation * self.level)
        self.writer.write(msg)
        self.writer.write("\n")

    def indent(self):
        self.level += 1

    def dedent(self):
        self.level -= 1

def iter_declarations(ffi):
    """Yield all declarations from an ffi object."""
    # Sometimes the source is a square bracket... related to ffi.include?
    for source in ffi._cdefsources:
        if source in '[]': continue
        ast = ffi._parser._parse(source)[0]
        for _, node in ast.children():
            if not isinstance(node, Decl):
                continue
            yield node

def get_declarations(ffi):
    return ffi._parser._declarations

def get_outargs(declaration):
    """
    Guess which arguments are output parameters by finding all primitive
    arguments at the end of a function's argument list.
    """
    outargs = {}
    for i in range(len(declaration.args) - 1, -1, -1):
        arg = declaration.args[i]
        if not is_primitive_p(arg):
            break
        if arg.get_c_name() in STRING_TYPES:
            break
        outargs[i] = arg
    return outargs

def funcnames_argnames(declarations):
    """
    Yield (function name, function argument names) for all functions in
    declarations.

    Some functions have parameters named None. This is either the void
    parameter or an unnamed parameter.
    """
    for declaration in declarations:
        if not isinstance(declaration.type, FuncDecl):
            continue
        funcname = declaration.name
        funcargs = list(p.name for p in declaration.type.args.params)
        for i, arg in enumerate(funcargs):
            if arg in ('from',):  # pesky Python keywords
                funcargs[i] = funcargs[i] + '_'
        yield funcname, funcargs

STRING_TYPES = ["char *", "char const *"]

class Builder(object):
    """
    Generate wrapper helpers based on some simple rules.
    """
    def __init__(self, funcdocs={}):
        """
        :param funcdocs: dict of {function name: docstring}.
        """
        self.all_funcdocs = funcdocs
        self.declarations_by_type = collections.defaultdict(list)

    def handle_enum(self, output, declaration_name, declaration):
        if not hasattr(declaration, "enumerators"):
            # it might be an anonymous struct
            return
        for name in declaration.enumerators:
            output.writeln("%s = _LIB.%s" % (name, name))
        output.writeln("")

    def handle_struct(self, output, declaration_name, declaration):
        c_name = declaration.get_c_name()
        output.writeln("class %s(Struct):" % c_name)
        output.indent()
        output.writeln('"""Wrap `%s`"""' % c_name)

        # Write struct properties as @property for better documentation
        for name in declaration.fldnames or []:
            output.writeln("@property")
            output.writeln("def %s(self): return self.cdata.%s" % (name, name))
            output.writeln("@%s.setter" % name)
            output.writeln("def %s(self, value): self.cdata.%s = value" % (name, name))

        # Add associated functions to struct:
        functions = self.declarations_by_type[c_name + " *"]
        for fname in functions:
            if fname[5].isupper():
                short_name = fname[4:]
            else:
                short_name = fname[4].lower() + fname[5:]
            output.writeln("%s = %s" % (short_name, fname))
        if not functions:
            output.writeln("pass")
        output.dedent()
        output.writeln("")

    def handle_function(self,
                        output,
                        declaration_name,
                        declaration,
                        arg_names):
        fname = declaration_name.split(' ')[1]

        if declaration.args:
            # take 'const' out of c name for this purpose.
            first_arg_name = declaration.args[0].get_c_name().replace('const ', '')
            self.declarations_by_type[first_arg_name].append(fname)

        outargs = get_outargs(declaration)

        # XXX filtering out the None parameter. Many of these are varargs functions
        # or logging functions that may not be necessary in our wrapper...
        # Later, compare to declaration.args, filter out void, and make names
        # for the varargs parameters.
        arg_names = list(name for name in arg_names if name)

        def arg_names_with_defaults():
            """
            Default primitive out-parameters to None, so cffi can allocate a
            new one to be returned.
            """
            for i, arg_name in enumerate(arg_names):
                if i in outargs:
                    yield "%s=None" % arg_name
                else:
                    yield arg_name

        arg_vars = ', '.join(arg_names_with_defaults())
        output.writeln("def %s(%s):" % (fname, arg_vars))
        output.indent()
        docstring = declaration.get_c_name().replace("(*)", " " + fname)
        output.writeln('"""')
        output.writeln("``" + docstring + "``")
        if fname in self.all_funcdocs:
            for doc_line in self.all_funcdocs[fname].splitlines():
                output.writeln(doc_line.rstrip())
        output.writeln('"""')

        for i, arg in enumerate(arg_names):
            c_arg = declaration.args[i]
            c_name = c_arg.get_c_name()
            if is_direct(c_arg):  # directly handled by cffi
                output.writeln("%s_c = %s" % (arg, arg))
            elif is_utf8(c_arg):
                output.writeln('%(arg)s_c = u8(%(arg)s)' % dict(arg=arg))
            else:
                null_ok = nullable.nullable.get(fname, ())
                output.writeln('%(arg)s_c = unbox(%(arg)s, %(c_name)r%(null_ok)s)' %
                               (dict(arg=arg, c_name=c_name,
                                     null_ok=(', nullable=True' if null_ok else ''))))

        line = []
        returns_void = isinstance(declaration.result, cffi.model.VoidType)
        if not returns_void:
            line.append("rc =")
        line.append("_LIB.%s(%s)" % (fname, ', '.join("%s_c" % arg for arg in arg_names)))
        output.writeln(" ".join(line))

        # handle errors
        error_handler = errorprone.handler_for_function(fname)
        if error_handler:
            output.writeln(error_handler)

        returning = []
        result_name = declaration.result.get_c_name()
        if returns_void:
            pass
        elif result_name in STRING_TYPES:
            returning.append("ffi.string(rc).decode('utf-8')")
        elif (result_name in ("void *", "struct _SDL_iconv_t *") or
              is_direct(declaration.result)):
            returning.append("rc")
        elif not is_primitive_or_primitive_p(declaration.result):
            match = re.match('(\w+_\w+)( const)?( *)', result_name)
            assert match
            if match:
                returning.append("%s(rc)" % match.group(1))
        else:
            returning.append("rc")

        for i, arg in enumerate(arg_names):
            # Assume all out-parameters are like int*, a single element.
            if i in outargs:
                returning.append("%s_c[0]" % arg)

        if len(returning) == 1:
            output.writeln("return %s" % returning[0])
        elif len(returning) > 1:
            output.writeln("return (%s)" % ", ".join(returning))

        output.dedent()
        output.writeln("")

    def generate(self,
                 output,
                 cdefs=None,
                 helpers=None,
                 filter=None):
        """
        Automatically generate libSDL2 wrappers by following some simple rules.
        Only used during build time.
        """
        sort_order = {'anonymous' : 3,
                      'function' : 0,
                      'struct' : 1,
                      'union' : 2,
                      'typedef' : 4 }

        argument_names = dict(funcnames_argnames(iter_declarations(cdefs.ffi)))

        def sort_key(declaration_name):
            kind, name = declaration_name.split()
            return (sort_order.get(kind, kind), name)

        declarations = get_declarations(cdefs.ffi)
        output = IndentedWriter(output)
        for declaration_name in sorted(declarations, key=sort_key):
            declaration = declarations[declaration_name]
            if filter and not filter.match(declaration_name):
                continue
            declaration_kind, declaration_n = declaration_name.split(" ")

            if declaration_kind == "function":
                self.handle_function(output,
                    declaration_name,
                    declarations[declaration_name],
                    argument_names[declaration_n])

            elif (declaration_kind == "typedef" and
                  hasattr(declaration, 'kind') and
                  declaration.kind in ("struct", "union")):
                self.handle_struct(output,
                    declaration_name,
                    declaration)

            elif declaration_kind in ("anonymous",):
                self.handle_enum(output,
                            declaration_name,
                            declarations[declaration_name])

            else:
                # print(declaration_name)
                pass
