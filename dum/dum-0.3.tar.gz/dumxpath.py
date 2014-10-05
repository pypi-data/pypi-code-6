import re
import collections


#
# Abstract base class
#
class Pth:
    def __init__(self, *paths):
        state = []
        for path in paths:
            cmds = compile_(path)
            result = []
            for c in cmds:
                bc = (getattr(self, c[0].__name__),)+c[1:]
                result.append(bc)
            state.append((0, tuple(result)))
        self.state = state

    def root(self, node):
        "/foo"
        raise NotImplementedError()

    def all(self, node):
        "//"
        raise NotImplementedError()

    def parent(self, node):
        ".."
        raise NotImplementedError()

    def attribvalue(self, node, attrib):
        "@attr"
        raise NotImplementedError()

    def attribtest(self, node, name, value):
        "foo[@attr=value]"
        raise NotImplementedError()

    def attribexist(self, node, attrib):
        "foo[@attr]"
        raise NotImplementedError()

    def index(self, node, name, index):
        "foo[1]"
        raise NotImplementedError()

    def name(self, node, name):
        "foo/name"
        raise NotImplementedError

    def value(self, obj):
        return obj


    def run_(self, stack, state):
        matches = collections.OrderedDict()
        for (idx, cmd) in state:
            try:
                c = cmd[idx]
            except IndexError:
                yield self.value(stack[-1])
                continue

            r = c[0](stack, *c[1:])

            if r is None:
                continue
            fstack, lasts = r
            if type(lasts) != list:
                lasts = (lasts,)
            for u in lasts:
                st = fstack+(u,)
                l = matches.setdefault(id(u), [st])  # FIXME : wrong key
                l.append((idx+1, cmd))
        for v in matches.values():
            yield from self.run_(v[0], v[1:])

    def __call__(self, obj):
        state = self.state[:]
        stack = (obj,)
        yield from self.run_(stack, state)
#
#  Compile xpath
#
PATTERN = re.compile(r'''((?:[^/"']|"[^"]*"|'[^']*')+)''')

FIRST = {
    '': None,  # select curent
    '/': (Pth.root,),
    '//': (Pth.all,),
}

SEP = {
    '/': None,
    '//': (Pth.all,),
}

ARGS = {
    '.': None,
    '..': (Pth.parent,),
}


def compile_arg_(arg, actions):
    try:
        actions.append(ARGS[arg])
        return
    except KeyError:
        pass

    if arg[:1] == "@":
        actions.append((Pth.attribvalue, arg[1:]))
        return

    if arg[-1:] != "]":
        actions.append((Pth.name, arg))
        return

    name, predicate = arg[:-1].split('[', 1)
    expression = predicate.split('=', 1)
    if len(expression) == 1:
        try:
            index = int(predicate)
        except ValueError:
            pass
        else:
            actions.append((Pth.index, name, index-1))
            return
        actions.append((Pth.name, name))
        if predicate[:1] == "@":
            actions.append((Pth.attribexist, predicate[1:]))
            return
        raise NotImplementedError()
    elif len(expression) == 2:
        actions.append((Pth.name, name))
        predicate, value = expression
        if predicate[:1] == "@":
            actions.append((Pth.attribtest, predicate[1:], value))
            return
        raise NotImplementedError()

    actions.append((Pth.name, name))
    raise NotImplementedError()


def compile_(path):
    actions = []
    items = iter(PATTERN.split(path))
    actions.append(FIRST[next(items)])

    while 1:
        cm = next(items)
        compile_arg_(cm, actions)

        sep = next(items)
        if not sep:
            break
        actions.append(SEP[sep])

    # optmize
    actions = [x for x in actions if x is not None]
    if actions[0][0] == Pth.root:
        actions = actions[1:]
    return tuple(actions)


#
#  Json support
#
class JsPath(Pth):
    def root(self, stack):
        return (), stack[0]

    def all(self, stack):
        raise NotImplementedError()

    def parent(self, stack):
        try:
            return stack[:-2], stack[-2]
        except IndexError:
            return None

    def attribexist(self, stack, name):
        if name in stack[-1]:
            return stack[:-1], stack[-1]

    def attribtest(self, stack, name, value):
        try:
            v = stack[-1][name]
        except KeyError:
            return None

        if v != value:
            return None
        return stack[:-1], stack[-1]

    def index(self, stack, name, index):
        obj = stack[-1]
        try:
            lst = obj[name]
        except KeyError:
            return None

        try:
            return stack[:1], lst[index]
        except IndexError:
            pass

    def name(self, stack, name):
        try:
            v = stack[-1][name]
        except KeyError:
            return None
        return stack, v
    attribvalue = name


#
#  XML (elementtree) support
#
class XmlPath(Pth):
    def root(self, stack):
        return (), stack[0]

    def all(self, stack):
        raise NotImplementedError()

    def parent(self, stack):
        try:
            return stack[:-2], stack[-2]
        except IndexError:
            return None

    def attribexist(self, stack, name):
        obj = stack[-1]
        if name in obj.attrib:
            return stack[:-1], stack[-1]

    def attribvalue(self, stack, name):
        obj = stack[-1]
        try:
            v = obj.attrib[name]
        except KeyError:
            return None
        return stack[:-1], v

    def attribtest(self, stack, name, value):
        obj = stack[-1]
        try:
            v = obj.attrib[name]
        except KeyError:
            return None

        if v != value:
            return None
        return stack[:-1], stack[-1]

    def index(self, stack, name, index):
        obj = stack[-1]
        for child in obj:
            if child.tag == name:
                if index>0:
                    index -= 1
                else:
                    return stack[:1], child

    def name(self, stack, name):
        obj = stack[-1]
        result = [c for c in obj if c.tag==name]
        return stack, result

    def value(self, obj):
        try:
            return obj.text
        except AttributeError:
            return obj

