"""Csv, Json and Xml projection to Python objects"""

import collections
import inspect
import xml.etree.ElementTree as ElementTree

import dumxpath

_DUM_NONE = object()  # no parsed value
_DUM_CONTENT = "dum_content"


#
# ##  TARGET ATTRIBUTES
#
class _AbstractTarget(object):
    # constants
    ATOM = 0
    NODE = 1
    LIST = 2
    GROUP = 3

    # defaults
    source = None
    attribname = None  # None:child or attr, False: only child, str: attr

    def fix_source(self, source):
        "split attribute and source path parts"
        items = source.rsplit("/@", 1)
        if len(items) == 2:
            self.source, self.attribname = items
        elif source == _DUM_CONTENT:
            self.source = "."
            self.attribname = False
        else:
            self.source = source
            if "/" in source:
                self.attribname = False

    def put(self, obj, value):
        "set value as obj attribute"
        setattr(obj, self.target, value)

    def set_default(self, obj):
        "set obj default attribute value"
        setattr(obj, self.target, self.default)


class _Atom(_AbstractTarget):
    """convert to a single value (int,str...)"""
    kind = _AbstractTarget.ATOM

    def __init__(self, convert, source=None, target=None, default=_DUM_NONE):
        self.parse = convert
        if source is not None:
            self.fix_source(source)
        self.target = target
        self.default = default

    def parse_xml(self, putfield, obj, child):
        defined_target = None
        if self.attribname:
            values = [child.attrib.get(self.attribname, None)]
        else:
            values = [child.text]
            if putfield.kind == _AbstractTarget.LIST:
                values += [gchild.tail for gchild in child]
        for value in values:
            if value is not None:
                childobj = self.parse(value)
                putfield.put(obj, childobj)
                defined_target = putfield.target
        return defined_target


class _Node(_AbstractTarget):
    """convert to a class"""
    kind = _AbstractTarget.NODE

    def __init__(self, cls, source=None, target=None, default=_DUM_NONE):
        self.cls = cls
        if source is not None:
            self.fix_source(source)
        self.target = target
        self.default = default

    def parse_xml(self, putfield, obj, child):
        childobj = _xml_parse_element(self.cls, child)
        putfield.put(obj, childobj)
        return putfield.target


class _List(_AbstractTarget):
    """convert to a list of objects"""
    kind = _AbstractTarget.LIST
    default = True

    def __init__(self, elemfield, source, target=None):
        self.elemfield = elemfield
        self.source = source
        self.target = target

    def put(self, obj, value):
        "set value in obj list attribute"
        try:
            lst = getattr(obj, self.target)
        except AttributeError:
            lst = []
            setattr(obj, self.target, lst)
        lst.append(value)

    def set_default(self, obj):
        "default is alwaus an empty list"
        setattr(obj, self.target, [])


class _Group(_List):
    "put several node types on the same list"
    kind = _AbstractTarget.GROUP
    target = None

    def __init__(self, kwds):
        self.kwds = {k: _field_initialize(v, k) for(k, v) in kwds.items()}

    def parse_xml(self, putfield, obj, child):
        defined_target = None

        txtfield = self.kwds.get(_DUM_CONTENT, None)
        if txtfield and child.text:
            childobj = txtfield.parse(child.text)
            putfield.put(obj, childobj)
            defined_target = putfield.target

        for node in child:
            try:
                sfield = self.kwds[node.tag]
            except KeyError:
                pass
            else:
                defined_target = sfield.parse_xml(putfield, obj, node)
            if txtfield and node.tail:
                childobj = txtfield.parse(node.tail)
                putfield.put(obj, childobj)
                defined_target = putfield.target

        return defined_target


#
# ## PRIVATE FUNCTIONS
#
def _field(value, source, default=_DUM_NONE):
    "low level field definition"
    # do we need to have it public ?
    if hasattr(value, "dum"):
        if inspect.isclass(value):
            return _Node(value, source=source, default=default)
        else:
            if default is _DUM_NONE:
                default = value
            return _Node(type(value), source=source, default=default)

    if isinstance(value, collections.Callable):
        return _Atom(value, source=source)
    if type(value) == list:
        if value:
            subfield = _field(value[0], source=source, default=default)
        else:
            subfield = _field(str, source=source, default=default)
        return _List(subfield, subfield.source)

    if default is _DUM_NONE:
        default = value
    return _Atom(type(value), source=source, default=default)


def _field_initialize(value, name):
    "initializing one dum field"
    if type(value) == tuple:
        value, source = value
    elif isinstance(value, _Group):
        source = "."
    else:
        source = name
    if isinstance(value, _AbstractTarget):
        if value.source is None:
            value.fix_source(source)
    else:
        value = _field(value, source)
    if value.target is None:
        value.target = name
    return value


def _bysources(cls):
    "lazy dum class initialization, return source paths"
    dum = cls.dum
    try:
        return dum.__bysources__
    except AttributeError:
        pass
    # initialize dum declaration
    bysources = []
    defaults = {}
    for name in dir(dum):
        if name.startswith("__") and name.endswith("__"):
            continue  # special methods
        value = getattr(dum, name)
        field = _field_initialize(value, name)

        bysources.append((field.source, field))
        if field.default is not _DUM_NONE:
            defaults[field.target] = field

    # TODO check for duplicated target ?
    dum.__bysources__ = bysources
    dum.__defaults__ = defaults

    return bysources


def _fix_defaults(obj, cls, defined_targets):
    "finalize obj : default values and dum_projection() call"
    defaults = [v for (k, v) in cls.dum.__defaults__.items()
                if k not in defined_targets]
    for field in defaults:
        field.set_default(obj)
    try:
        dum_projection = obj.dum_projection
    except AttributeError:
        return obj
    return dum_projection()


#
# ## CONVERTER DECORATORS
#
def converter(source=None, default=_DUM_NONE):
    """decorator for dum atom field defintion"""
    if isinstance(source, collections.Callable):
        # called without attributes
        return _Atom(convert=source, default=default)

    def _converter(convert):
        return _Atom(convert=convert, source=source, default=default)
    return _converter


def lister(source=None):
    """decorator for dum list field defintion"""
    if isinstance(source, collections.Callable):
        # called without attributes
        subfield = _field(source, source=source.__name__)
        return _List(subfield, source.__name__)

    def _lister(convert):
        subfield = _field(convert, source=source)
        return _List(subfield, source)
    return _lister


def group(dum_map={}, **kwds):
    """collect several child node in one list"""
    kwds.update(dum_map)
    return _Group(kwds)


#
# ##  CSV PARSING
#
def csv(cls, rows, headers=None):
    """Csv parsing"""
    rows = iter(rows)
    # dum declaration
    bysources = dict(_bysources(cls))
    defined_targets = set()
    # column headers
    fields = []
    if headers is None:
        headers = next(rows)  # assume headers are in the first row
    for i, source in enumerate(headers):
        try:
            field = bysources[source]
        except KeyError:
            continue
        fields.append((i, field))
        defined_targets.add(field.target)
    # actual paring
    for row in rows:
        obj = cls()
        for i, field in fields:
            v = field.parse(row[i])
            field.put(obj, v)
        yield _fix_defaults(obj, cls, defined_targets)


#
# ##  JSON PARSING
#
def json(cls, values):
    """Json parsing"""
    bysources = _bysources(cls)
    defined_targets = set()
    obj = cls()
    for key, field in bysources:
        putfield = field
        if field.kind == field.LIST:
            field = field.elemfield
        jxpath = dumxpath.JsPath(key)
        for v in jxpath(values):
            if field.kind == field.ATOM:
                childobj = field.parse(v)
            elif field.kind == field.NODE:
                childobj = json(field.cls, v)
            else:
                raise TypeError("unknown field type")
            putfield.put(obj, childobj)
            defined_targets.add(putfield.target)
            if putfield.kind != putfield.LIST:
                break
    return _fix_defaults(obj, cls, defined_targets)


#
# ## XML PARSING
#

def _xml_parse_element(cls, elmt):
    bysources = _bysources(cls)
    defined_targets = set()
    obj = cls()

    # namespaces
    try:
        namespaces = cls.dum.__namespaces__
    except AttributeError:
        namespaces = {}
    try:
        prefix = cls.dum.__default_namespace__
    except AttributeError:
        pass
    else:
        prefix = "{%s}" % prefix
        for node in elmt.iter():
            node.tag = node.tag.replace(prefix, "")

    # children
    attribs = []
    for match, field in bysources:
        putfield = field
        if field.kind == field.LIST:
            field = field.elemfield
            children = elmt.findall(match, namespaces=namespaces)
        else:
            child = elmt.find(match, namespaces=namespaces)
            if child is None:
                if field.attribname is None:
                    attribs.append((match, field))
                continue
            children = (child,)

        for child in children:
            defined_target = field.parse_xml(putfield, obj, child)
            defined_targets.add(defined_target)

    # curent node attributes
    for key, field in attribs:
        try:
            value = elmt.attrib[key]
        except KeyError:
            continue
        putfield = field
        if field.kind == field.LIST:
            field = field.elemfield

        if field.kind == field.ATOM:
            childobj = field.parse(value)
        else:
            # TODO put value in node.dum_content ?
            raise ValueError("attr can't map to node "+putfield.target)
        putfield.put(obj, childobj)
        defined_targets.add(putfield.target)
    return _fix_defaults(obj, cls, defined_targets)


def xmls(cls, txt):
    """Xml string parsing"""
    root = ElementTree.fromstring(txt)
    return _xml_parse_element(cls, root)


def xml(cls, fd):
    """Xml file parsing"""
    tree = ElementTree.parse(fd)
    root = tree.getroot()
    return _xml_parse_element(cls, root)
