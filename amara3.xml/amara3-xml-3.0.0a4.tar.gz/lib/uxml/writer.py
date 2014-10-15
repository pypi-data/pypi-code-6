'''
Raw XML writer
'''

from enum import Enum #https://docs.python.org/3.4/library/enum.html

class token(Enum):
    start_open = 1
    start_close = 2
    end_open = 3
    end_close = 4
    attr_quote = 5
    pre_attr_space = 6
    attr_equals = 7


TOKENS = {
    token.start_open: '<',
    token.start_close: '>',
    token.end_open: '</',
    token.end_close: '>',
    token.attr_quote: '"',
    token.pre_attr_space: ' ',
    token.attr_equals: '=',
}


class context(Enum):
    start_element = 1
    end_element = 2
    text = 3


class raw(object):
    '''
    >>> import io
    >>> from amara3.uxml import writer
    >>> fp = io.StringIO() #or is it better to use BytesIO?
    >>> w = writer.raw(fp)
    >>> w.start_element('spam')
    >>> w.text('eggs')
    >>> w.end_element('spam')
    >>> fp.getvalue()
    '<spam>eggs</spam>'   
    '''
    def __init__(self, fp=None, whandler=None):
        #FIXME: check that fp *or* whandler are not None
        self._fp = fp
        self._whandler = whandler(fp) or self
        return

    def write(self, context, text):
        if isinstance(text, token): text = TOKENS[text]
        self._fp.write(text)
        return

    def start_element(self, name, attribs=None):
        attribs = attribs or {}
        ctx = context.start_element
        self._whandler.write(ctx, token.start_open)
        self._whandler.write(ctx, name)
        for k, v in attribs:
            self._whandler.write(ctx, token.pre_attr_space)
            self._whandler.write(ctx, k)
            self._whandler.write(ctx, token.attr_equals)
            self._whandler.write(ctx, token.attr_quote)
            self._whandler.write(ctx, v)
            self._whandler.write(ctx, token.attr_quote)
        self._whandler.write(ctx, token.start_close)
        return

    def end_element(self, name):
        ctx = context.end_element
        self._whandler.write(ctx, token.end_open)
        self._whandler.write(ctx, name)
        self._whandler.write(ctx, token.end_close)
        return

    def text(self, text):
        ctx = context.text
        self._whandler.write(ctx, text)
        return


class nsfilter(object):
    '''
    >>> import io
    >>> from amara3.uxml import writer
    >>> fp = io.StringIO()
    >>> w = writer.raw(fp)
    >>> w.start_element('spam')
    >>> w.text('eggs')
    >>> w.end_element('spam')
    >>> fp.getvalue()
    '<spam>eggs</spam>'   
    '''
    def __init__(self, fp, mapping=None):
        self._mapping = mapping or {}
        self._fp = fp
        return

    def write(self, context, text):
        self._fp.write(text)
        if context in (context.start_element, context.end_element):
            if text:
                pass
        elif 1:
            isinstance(text, token): text = TOKENS[text]
        return

    def start_element(self, name, attribs=None):
        attribs = attribs or {}
        ctx = 
        self._whandler.write(ctx, token.start_open)
        self._whandler.write(ctx, name)
        for k, v in attribs:
            self._whandler.write(ctx, token.pre_attr_space)
            self._whandler.write(ctx, k)
            self._whandler.write(ctx, token.attr_equals)
            self._whandler.write(ctx, token.attr_quote)
            self._whandler.write(ctx, v)
            self._whandler.write(ctx, token.attr_quote)
        self._whandler.write(ctx, token.start_close)
        return

    def end_element(self, name):
        ctx = context.end_element
        self._whandler.write(ctx, token.end_open)
        self._whandler.write(ctx, name)
        self._whandler.write(ctx, token.end_close)
        return

    def text(self, text):
        ctx = context.text
        self._whandler.write(ctx, text)
        return
