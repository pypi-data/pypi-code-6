from collections import defaultdict
try:
    from ast import iter_child_nodes
except ImportError:   # Python 2.5
    from flake8.util import iter_child_nodes

__version__ = '0.1'


EXCEPTIONS = []


class ASTVisitor(object):

    """Performs a depth-first walk of the AST."""

    def __init__(self):
        self.node = None
        self._cache = {}

    def default(self, node, *args):
        for child in iter_child_nodes(node):
            self.dispatch(child, *args)

    def dispatch(self, node, *args):
        self.node = node
        klass = node.__class__
        meth = self._cache.get(klass)
        if meth is None:
            className = klass.__name__
            meth = getattr(self.visitor, 'visit' + className, self.default)
            self._cache[klass] = meth
        return meth(node, *args)

    def preorder(self, tree, visitor, *args):
        """Do preorder walk of tree using visitor."""
        self.visitor = visitor
        visitor.visit = self.dispatch
        self.dispatch(tree, *args)


class PathNode(object):
    def __init__(self, name, look="circle"):
        self.name = name
        self.look = look


class PathGraph(object):
    def __init__(self, name, entity, lineno):
        self.name = name
        self.entity = entity
        self.lineno = lineno
        self.nodes = defaultdict(list)
        self.needs_conversion = False


class PathGraphingAstVisitor(ASTVisitor):

    """A visitor for a parsed Abstract Syntax Tree."""

    def __init__(self):
        super(PathGraphingAstVisitor, self).__init__()
        self.classname = ""
        self.graphs = {}

    def dispatch_list(self, node_list):
        for node in node_list:
            self.dispatch(node)

    def visitFunctionDef(self, node):

        if self.classname:
            entity = '%s%s' % (self.classname, node.name)
        else:
            entity = node.name

        name = '%d:1: %r' % (node.lineno, entity)

        self.graph = PathGraph(name, entity, node.lineno)
        self.graphs["%s%s" % (self.classname, node.name)] = self.graph

        if node.decorator_list and self.classname not in EXCEPTIONS:
            for decorator in node.decorator_list:
                if (hasattr(decorator, 'func') and
                        hasattr(decorator.func, 'attr') and
                        hasattr(decorator.func, 'value') and
                        hasattr(decorator.func.value, 'id') and
                        ("%s.%s" % (decorator.func.value.id,
                                    decorator.func.attr) == 'mock.patch')):
                            self.graph.needs_conversion = True

    def visitClassDef(self, node):
        old_classname = self.classname
        self.classname += node.name + "."
        self.dispatch_list(node.body)
        self.classname = old_classname


class DoublesChecker(object):

    """Check whether tests are written using doubles."""

    name = 'flake8_doubles'
    version = __version__
    _error_tmpl = "Z011 %s is not written using doubles"

    def __init__(self, tree, filename):
        self.tree = tree

    @classmethod
    def add_options(cls, parser):
        parser.add_option('--doubles_exceptions', default="", action='store',
                          type='string', help="Flake8 checker for doubless")
        parser.config_options.append('doubles_exceptions')

    @classmethod
    def parse_options(cls, options):
        for clazz in options.doubles_exceptions.split(','):
            EXCEPTIONS.append(clazz + '.')

    def run(self):
        visitor = PathGraphingAstVisitor()
        visitor.preorder(self.tree, visitor)
        for graph in visitor.graphs.values():
            if graph.needs_conversion:
                text = self._error_tmpl % graph.entity
                yield graph.lineno, 0, text, type(self)
