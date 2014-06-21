import ast
import textwrap
import tokenize
from collections import namedtuple
from tokenize import COMMENT, DEDENT, ENDMARKER, INDENT, NEWLINE, STRING, NAME


class Name(namedtuple('Name', 'name asname')):
    CAMEL, SNAKE, CONST = range(3)

    @property
    def kind(self):
        name = self.name.split('.')[-1]
        if name.isupper():
            return self.CONST
        if name[0].isupper():
            return self.CAMEL
        return self.SNAKE

    def key(self):
        return self.kind, str(self)

    def __str__(self):
        if self.asname:
            return '{0} as {1}'.format(self.name, self.asname)
        return self.name


class Import(namedtuple('Import', 'kind module names noqa start end')):

    def merge(self, other):
        names = sorted(set(self.names + other.names), key=Name.key)
        noqa = self.noqa or other.noqa
        return Import(self.kind, self.module, names, noqa, -1, -1)


Block = namedtuple('Block', 'imports indent start')


def parse_imports(lines):
    it = iter(lines)
    tokens = (_TokenInfo(*token) for token in
              tokenize.generate_tokens(lambda: next(it)))

    parser = _ImportParser(tokens, lines)
    return parser.parse_block('', 0)


class _TokenInfo(namedtuple('TokenInfo', 'type string start end line')):
    @property
    def name(self):
        return self.type == NAME and self.string

    @property
    def starts_block(self):
        return self.type == INDENT

    @property
    def ends_block(self):
        return self.type in (DEDENT, ENDMARKER)


class _ImportParser(namedtuple('_ImportParser', 'tokens lines')):
    def parse_block(self, indent, start):
        imports = []
        token = next(self.tokens)

        # Push imports beneath docstring
        if token.type == STRING:
            start = token.end[0] + 1
            token = next(self.tokens)

        while not token.ends_block:
            if token.starts_block:
                self.parse_block(token.string, token.start[0] - 1)
            elif token.name in ('from', 'import'):
                imports += self.parse_imports(token)
            token = next(self.tokens)

        if imports:
            # wrong
            yield Block(imports, indent, start)

    def parse_imports(self, token):
        first = token
        comments = []
        while token.type != NEWLINE:
            if token.type == COMMENT:
                comments.append(token.string)
            token = next(self.tokens)

        start, end = first.start[0] - 1, token.end[0]
        source = '\n'.join(self.lines[start:end])
        nodes = ast.parse(textwrap.dedent(source)).body
        # TODO: error on multiple nodes
        return self._make_imports(first.name, nodes[0], comments, start, end)

    @staticmethod
    def _make_imports(kind, node, comments, start, end):
        noqa = any(c.startswith('# noqa') for c in comments)
        names = sorted([Name(n.name, n.asname)
                        for n in node.names], key=Name.key)
        if kind == 'from':
            modules = [Name(node.module, None)]
        else:
            modules, names = names, []

        return [Import(kind, m, names, noqa, start, end) for m in modules]
