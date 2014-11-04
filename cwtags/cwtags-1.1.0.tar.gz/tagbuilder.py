"""helper classes to generate simple (X)HTML tags for use in CubicWeb (tm)

Tags
----

provides tags supporting two usages :

* functional nesting, as in::

   w = self.w
   w(table(tr(th(u'header, col1'),
              th(u'header, col2')),
           tr(td(u'row2, col1'),
              td(u'row2, col2')))

* imperative nesting, as in::

   w = self.w
   with table(w) as t:
       with tr(t) as r:
           r(th(u'header, col1'))
           r(th(u'header, col2'))
       with tr(t) as r:
           r(td(u'row1, col1'))
           r(td(u'row1, col2'))

The point of the second notation is to be able to interleave html
building with statements::

   with table(w, id=u'foo') as t:
       with tr(t) as r:
           r(th(u'header, col1'))
       with tr(t):
           self.render_entity_attributes(entity)

... where the called method will actually write its stuff in the
second table row.

Attributes
----------

The tag attributes are passed as keywords arguments.

Their names will be lowercased, and any prefix/postfix '_' character will be
stripped. This is useful for reserved python words like 'class'.
For the 'class' attribute, 'klass' is also supported.

For ex:

    div(Class='css') == div(class_='css') == div(_class='css') == div(klass='css')

An attribute value can be :

*   a string -> copied verbatim
*   True -> the attribute is added with no value
*   False, None -> the attribute is not added
*   list, tuple, set, frozenset -> joined with a whitespace
*   dict -> keys having a non-false value are joined with a whitespace

Examples:

>>> tag.div(class_={'css1': True, 'css2': False})
u'<div class="css1"></div>'
>>> tag.div(class_=('css1', 'css2'))
u'<div class="css1 css2"></div>'
>>> tag.option("Ten", value='10', selected=True)
u'<option selected value="10">Ten</option>'
>>> tag.option("Ten", value='10', selected=False)
u'<option value="10">Ten</option>'


:organization: Logilab
:copyright: 2009 LOGILAB S.A. (Paris, FRANCE), license is LGPL v2.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
:license: GNU Lesser General Public License, v2.1 - http://www.gnu.org/licenses
"""
__docformat__ = "restructuredtext en"
from logilab.common.decorators import monkeypatch

HTML_EMPTY_TAGS = frozenset(('area', 'base', 'col', 'meta', 'hr', 'br',
                             'img', 'input', 'link', 'param'))


def translate_attr(name, value):
    name = name.lower().replace('__', ':')
    name = name.strip('_').replace('_', '-')
    if name == 'klass':
        name = 'class'
    if isinstance(value, (list, tuple, set, frozenset)):
        value = u' '.join(value)
    elif isinstance(value, dict):
        value = u' '.join(k for k, v in value.items() if v)
    return name, value


def build_attrs(attr_dict):
    return u' '.join(k if v is True else '%s="%s"' % (k, v)
                     for k, v in (
                         translate_attr(k, v)
                         for k, v in attr_dict.iteritems())
                     if v not in (None, False))


class simpletag(object):
    __slots__ = ('_unicode')

    def __init__(self, name, children, kwargs):
        if kwargs:
            self._unicode = u'<%(tag)s %(attrs)s>%(children)s</%(tag)s>' % {
                'tag'  : name, 'attrs' : build_attrs(kwargs),
                'children': u''.join(unicode(child) for child in children)}
        else:
            self._unicode = u'<%(tag)s>%(children)s</%(tag)s>' % {
                'tag'  : name,
                'children': u''.join(unicode(child) for child in children)}

    def __unicode__(self):
        return self._unicode
    def __str__(self):
        return self._unicode.encode('utf-8')
    def __repr__(self):
        return repr(self._unicode)

    # Not a true context manager, but someone using this as one:
    # with div(id=42):
    #     ...
    # instead of
    # with div(w, id=42):
    #    ...
    # Would get a nasty error. Instead we make a polite suggestion.
    def __enter__(self):
        raise TypeError('Did you forget to give a callable in first position ?')
    def __exit__(self, exc_type, exc_value, traceback):
        pass


class emptytag(simpletag):
    __slots__ = ('_unicode')

    def __init__(self, name, _children, kwargs):
        assert not len(_children) and len(kwargs)
        self._unicode = u'<%(tag)s %(attrs)s/>' % {'tag'  : name,
                                                   'attrs' : build_attrs(kwargs)}

class contexttag(object):

    def __init__(self, parent, name, kwargs):
        self.parent = parent
        if kwargs:
            self.opening = u'<%s %s>' % (name, build_attrs(kwargs))
        else:
            self.opening = u'<%s>' % name
        self.closing = u'</%s>\n' % name

    def __repr__(self):
        return '%s...%s' % (self.opening, self.closing)

    def __call__(self, node):
        self.parent(node)
    write = __call__ # UStringIO api

    def __enter__(self):
        self.parent(self.opening)
        return self
    def __exit__(self, _type, _value, _tb):
        self.parent(self.closing)

def tag(name):
    basetag = simpletag
    if name in HTML_EMPTY_TAGS:
        basetag = emptytag
    def tag_builder(*args, **kwargs):
        parent = args and args[0]
        if parent and callable(parent):
            return contexttag(parent, name, kwargs)
        return basetag(name, args, kwargs)
    return tag_builder

try:
    from cubicweb.utils import UStringIO
except ImportError:
    class UStringIO(list):
        def getvalue(self):
            return u''.join(self)


_write = UStringIO.write

@monkeypatch(UStringIO)
def write(self, value):
    if isinstance(value, (simpletag, contexttag)):
        return _write(self, unicode(value))
    return _write(self, value)
