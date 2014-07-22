"""
Put a Pythonic face on estraiernative
"""
import sys
from HTMLParser import HTMLParser
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from _estraiernative import (Condition as CCondition,
    Database as CDatabase, Document as CDocument, EstError as CError)

class FlushFailed(Exception):
    """
    Could not remove the specified doc from the database.
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class EditFailed(Exception):
    """
    Could not edit the specified doc in the database
    """
    def __init__(self, id, msg):
        self.id = id
        self.msg = msg

    def __str__(self):
        return 'Document %s: %s' % (self.id, self.msg)

class PutFailed(Exception):
    """
    Could not add the specified doc to the database.
    """
    def __init__(self, uri, msg):
        self.uri = uri
        self.msg = msg

    def __str__(self):
        return 'Document %s: %s' % (self.uri, self.msg)

class OpenFailed(Exception):
    """
    Could not open the database with the specified mode.
    """
    def __init__(self, *args):
        self.msg = args[0]

    def __str__(self):
        return self.msg

class CloseFailed(Exception):
    """
    Could not close the database.
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def enforceUnicode(s, argName, exceptionClass, encoding='utf8'):
    """
    Force s to be a unicode object or None; return a byte string
    """
    if s is None:
        return None
    if not type(s) is unicode:
        raise exceptionClass('%s must be unicode' % (argName,))
    return s.encode(encoding)

def unicodeToByte(argSpecs, exceptionClass):
    """
    Test each of the argNames to see whether they are unicode text objects.
    If they are not, raise exceptionClass
    """
    def decorator(fn):
        def wrapper(*a, **kw):
            a = list(a)
            for pos, name in argSpecs:
                if name in kw:
                    kw[name] = enforceUnicode(kw[name], name, exceptionClass)
                else:
                    if len(a) >= pos + 1:
                        a[pos] = enforceUnicode(a[pos], name, exceptionClass)
            return fn(*a, **kw)
        return wrapper

    return decorator


class HCondition(object):
    """
    A search condition.
    Use matching='simple', 'rough', 'union' or 'isect'
    """
    @unicodeToByte([(1,'phrase')], TypeError)
    def __init__(self, phrase=None, matching='simple', max=None, skip=None):
        self.condition = CCondition()
        if phrase is not None:
            self.condition.set_phrase(phrase)
        if max is not None:
            self.condition.set_max(max)
        if skip is not None:
            self.condition.set_skip(skip)
        flags = 0
        if matching == 'simple':
            flags |= CCondition.SIMPLE
        elif matching == 'rough':
            flags |= CCondition.ROUGH
        elif matching == 'union':
            flags |= CCondition.UNION
        elif matching == 'isect':
            flags |= CCondition.ISECT
        self.condition.set_options(flags)

    @unicodeToByte([(1,'expression')], TypeError)
    def addAttr(self, expression):
        """
        Use 'expression' to filter results by attributes
        """
        self.condition.add_attr(expression)

    @unicodeToByte([(1,'expression')], TypeError)
    def setOrder(self, expression):
        """
        Use 'expression' to order results by attributes
        """
        self.condition.set_order(expression)


class HDatabase(object):
    """
    A more pythonic interface to estraier's database

    With autoflush=True (the default), automatically flush after every
    document add, which simplifies indexing.

    Set autoflush=False to manually flush, which allows better performance
    when indexing lots of documents at once.

    Per http://hyperestraier.sourceforge.net/uguide-en.html Hyper Estraier
    expects data to be stored as utf-8 bytes.  Therefore, there is no encoding
    parameter.
    """
    def __init__(self, autoflush=False):
        self._cdb = CDatabase()
        self.autoflush = autoflush

    def putDoc(self, doc, clean=False, weight=False):
        """
        Add a document to the index
        """
        flags = 0
        if clean:
            flags = flags | self._cdb.PDCLEAN
        if weight:
            flags = flags | self._cdb.PDWEIGHT
        if not self._cdb.put_doc(doc._cdoc, flags):
            msg = self._cdb.err_msg(self._cdb.error())
            raise PutFailed(doc[u'@uri'], msg)

        if self.autoflush:
            self.flush()

        return doc

    def flush(self):
        """
        Write documents to disk and break them into words
        """
        failed = False
        try:
            self._cdb.flush(-1)
        except CError:
            failed = True
        if failed:
            msg = self._cdb.err_msg(self._cdb.error())
            raise FlushFailed(msg)

    @unicodeToByte([(2,'uri')], TypeError)
    def remove(self, doc=None, uri=None, id=None):
        """
        Take a document out of the database by reference, by uri or by id
        """
        if uri is None and id is None and doc is None:
            raise TypeError("Either doc, uri or id is required to remove a document")

        flags = 0 # TODO - support ODCLEAN flag
        if hasattr(doc, 'id'):
            id = doc.id
        else:
            if uri is not None:
                id = self._cdb.uri_to_id(uri)
        if not self._cdb.out_doc(id, flags):
            msg = self._cdb.err_msg(self._cdb.error())
            raise EditFailed(id, msg)

    def __delitem__(self, uri):
        return self.remove(uri=uri)

    def updateAttributes(self, doc):
        """
        Edit a document's attributes in-place.  Note: there is no way to edit
        the texts.
        """
        failed = False
        try:
            self._cdb.edit_doc(doc._cdoc)
        except CError:
            failed = True
        if failed:
            msg = self._cdb.err_msg(self._cdb.error())
            raise EditFailed(doc.id, msg)

    def optimize(self, purge=False, opt=False):
        """
        Perform either a free-space compact operation, or a db optimization,
        or both, or neither, depending on flags.
        """
        flags = (0 if purge else self._cdb.OPTNOPURGE)
        flags = flags | (0 if opt else self._cdb.OPTNODBOPT)
        self._cdb.optimize(flags)

    def __len__(self):
        return self._cdb.doc_num()

    def sync(self):
        """
        ??? If anyone knows what this should do and how it is different from
        flush(), tell me.
        """
        raise NotImplementedError("I'll implement this when someone tells me what it does")
        self._cdb.sync() # TODO - needs a unit test

    def open(self, directory, mode):
        """
        Open the database directory.  Only valid modes are 'a', 'r' and 'w'

        'a' corresponds to WRITER | CREAT (created only if it does not exist)
        'w' corresponds to WRITER | CREAT | TRUNC (clobbered if it exists)
        'r' corresponds to READER
        """
        flags = 0
        if mode == 'a':
            flags = self._cdb.DBWRITER | self._cdb.DBCREAT
        elif mode == 'w':
            flags = self._cdb.DBWRITER | self._cdb.DBCREAT | self._cdb.DBTRUNC
        elif mode == 'r':
            flags = self._cdb.DBREADER

        assert flags, "mode must be 'a', 'w' or 'r'"

        if not self._cdb.open(directory, flags):
            msg = self._cdb.err_msg(self._cdb.error())
            raise OpenFailed(msg)

        return self

    def close(self):
        """
        Put the database down for the night.
        """
        failed = False
        try:
            self._cdb.close()
        except CError:
            failed = True
        if failed:
            msg = self._cdb.err_msg(self._cdb.error())
            raise CloseFailed(msg)

    def search(self, condition):
        """
        Submit a query to the database and return the results object.
        """
        result = self._cdb.search(condition.condition)
        return HResults(self, result)

    def walkResult(self, result):
        """
        Produce a HHit for each doc in the result
        """
        count = result.doc_num()
        for i in range(count):
            doc = self._cdb.get_doc(result.get_doc_id(i), 0) # TODO - flags

            if doc is None: # XXX WTF? is this for a race condition against
                continue    # someone removing docs from the index?

            yield HHit.fromCDocument(doc)

    @unicodeToByte([(1,'uri')], KeyError)
    def __getitem__(self, uri):
        id = self._cdb.uri_to_id(uri)
        return HDocument.fromCDocument(self._cdb.get_doc(id, 0))

    def __iter__(self):
        cond = HCondition()
        cond.addAttr(u'@id')
        return iter(self.search(cond))


class HResults(list):
    """
    List wrapper for results of the search.
    """
    def __init__(self, db, result):
        self._cresult = result
        list.__init__(self, db.walkResult(result))

    def hintWords(self):
        """
        Return the unicode-d search terms
        """
        return [w.decode('utf-8') for w in self._cresult.hint_words()]

    def pluck(self, attribute):
        """
        Return the value of the given attribute for each result, in a list
        """
        return [h[attribute] for h in self]


class HDocument(object):
    """
    Dict-like interface to a document

    >>> doc = HDocument(u'http://sample.com/page.html')
    """
    def __str__(self):
        return self._cdoc.dump_draft()

    @unicodeToByte([(1,'uri')], TypeError)
    def __init__(self, uri):
        self._cdoc = CDocument()
        self._cdoc.add_attr('@uri', uri.replace('\0', ''))

    @unicodeToByte([(1,'text')], TypeError)
    def addHiddenText(self, text):
        """
        Add text that will affect search scoring but will NOT appear in the
        output document
        """
        self._cdoc.add_hidden_text(text.replace('\0', ''))

    @unicodeToByte([(1,'text')], TypeError)
    def addText(self, text):
        """
        Put some text into the document
        """
        self._cdoc.add_text(text.replace('\0', ''))

    @classmethod
    def fromCDocument(cls, cdocument):
        """
        Construct a document from an existing estraiernative.Document, such as
        when iterating search results.
        """
        self = cls(uri=cdocument.attr('@uri').decode('utf8'))
        self._cdoc = cdocument
        return self

    def __delitem__(self, name):
        raise NotImplementedError("Cannot delete attributes from this document")

    @unicodeToByte([(1,'name'), (2,'value')], TypeError)
    def __setitem__(self, name, value):
        self._cdoc.add_attr(name.replace('\0', ''),
                value.replace('\0', ''))

    @unicodeToByte([(1,'name')], KeyError)
    def __getitem__(self, name):
        if name not in self._cdoc.attr_names():
            raise KeyError(name)
        return self._cdoc.attr(name).decode('utf-8')

    def update(self, other):
        """
        Update attributes of this document from another one
        """
        for k, v in other.items():
            self[k] = v

    def get(self, key, default=None):
        """
        Return doc[key] unless key is not found, in which case return the
        value of 'default' (None unless specified)
        """
        try:
            return self[key]
        except KeyError:
            return default

    def keys(self):
        """
        Names of all attributes set on this document
        """
        return [n.decode('utf-8') for n in self._cdoc.attr_names()]

    def values(self):
        """
        Values of all attributes set on this document
        """
        return [self[a] for a in self.keys()]

    def items(self):
        """
        (attribute_name, attribute_value) 2-tuples for every attribute in this
        document
        """
        return [(a,self[a]) for a in self.keys()]

    def getTexts(self):
        """
        Return all (visible) texts in this document, as a list
        """
        return map(lambda t: t.decode('utf-8'), self._cdoc.texts())

    def _get_text(self):
        return u'\n'.join(self.getTexts())
    text = property(_get_text)

    def _get_id(self):
        return self._cdoc.id()
    id = property(_get_id)

    def encode(self, encoding):
        """
        Return an encoded version of this document.  Convenience method
        """
        return ''.join([s.encode(encoding) for s in self.getTexts()])


class HHit(HDocument):
    """
    A hit returned by a search.
    """

    teaserFormats = 'html rst'.split()

    def emphasize_html(self, text):
        """
        Write emphasized text in html
        """
        return '<strong>%s</strong>' % text

    def emphasize_rst(self, text):
        """
        Write emphasized text in restructuredtext
        """
        return '**%s**' % text

    def teaser(self, terms, format='html'):
        """
        Produce the teaser/snippet text for the hit
        """
        if format not in self.teaserFormats:
            raise NotImplementedError( "Supported formats are: %s" % (
                ', '.join(self.teaserFormats),))

        emph = getattr(self, 'emphasize_%s' % (format,))

        # arguments to make_snippet MUST be byte strings
        bterms = []
        for t in terms:
            if not type(t) is type(u''):
                raise TypeError("Terms must be unicode text")
            bterms.append(t.encode('utf8'))

        # TODO - parameterize make_snippet's numbers
        snip = self._cdoc.make_snippet(bterms, 120, 35, 35)

        # parse the newline-delimited snippet format
        bunches = snip.split('\n\n')
        strings = []
        for bunch in snip.split('\n\n'):
            _bitStrings = []
            for bit in bunch.split('\n'):
                if '\t' in bit:
                    _bitStrings.append(emph(bit.split('\t')[0]))
                else:
                    _bitStrings.append(bit)
            strings.append(''.join(_bitStrings))

        decode = lambda s: unicode(s, 'utf8')
        snip = u' ... '.join(map(decode, strings))
        return snip
