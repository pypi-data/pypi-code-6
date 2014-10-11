# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2008
import re
import string
from six.moves.html_entities import name2codepoint
from six import unichr, PY2


# Configuration for add_links() function
LEADING_PUNCTUATION  = ['(', '<', '&lt;']
TRAILING_PUNCTUATION = ['.', ',', ')', '>', '\n', '&gt;', "'", '"']

# list of possible strings used for bullets in bulleted lists
DOTS = ['&middot;', '*', '\xe2\x80\xa2', '&#149;', '&bull;', '&#8226;']

unencoded_ampersands_re = re.compile(r'&(?!(\w+|#\d+);)')
word_split_re = re.compile(r'(\s+)')
punctuation_re = re.compile('^(?P<lead>(?:%s)*)(?P<middle>.*?)(?P<trail>(?:%s)*)$' % \
    ('|'.join([re.escape(x) for x in LEADING_PUNCTUATION]),
    '|'.join([re.escape(x) for x in TRAILING_PUNCTUATION])))
simple_email_re = re.compile(r'^\S+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+$')
link_target_attribute_re = re.compile(r'(<a [^>]*?)target=[^\s>]+')
html_gunk_re = re.compile(r'(?:<br clear="all">|<i><\/i>|<b><\/b>|<em><\/em>|<strong><\/strong>|<\/?smallcaps>|<\/?uppercase>)', re.IGNORECASE)
hard_coded_bullets_re = re.compile(r'((?:<p>(?:%s).*?[a-zA-Z].*?</p>\s*)+)' % '|'.join([re.escape(x) for x in DOTS]), re.DOTALL)
trailing_empty_content_re = re.compile(r'(?:<p>(?:&nbsp;|\s|<br \/>)*?</p>\s*)+\Z')
if PY2:
    del x # Temporary variable

def escape(html):
    '''
    Returns the given HTML with ampersands, quotes and carets encoded

    >>> escape('html "test" & <brothers>')
    'html &quot;test&quot; &amp; &lt;brothers&gt;'
    '''
    if not isinstance(html, basestring):
        html = str(html)
    return html.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')

def linebreaks(value):
    '''
    Converts newlines into <p> and <br />
    '''
    value = re.sub(r'\r\n|\r|\n', '\n', value) # normalize newlines
    paras = re.split('\n{2,}', value)
    paras = ['<p>%s</p>' % p.strip().replace('\n', '<br />') for p in paras]
    return '\n\n'.join(paras)

def strip_tags(value):
    """
    Returns the given HTML with all tags stripped
    
    >>> strip_tags('some <h2>title</h2> <script>asdfasdf</script>')
    'some title asdfasdf'
    """
    return re.sub(r'<[^>]*?>', '', value)

stripTags = strip_tags

def strip_spaces_between_tags(value):
    "Returns the given HTML with spaces between tags normalized to a single space"
    return re.sub(r'>\s+<', '> <', value)

def strip_entities(value):
    "Returns the given HTML with all entities (&something;) stripped"
    return re.sub(r'&(?:\w+|#\d);', '', value)

def fix_ampersands(value):
    "Returns the given HTML with all unencoded ampersands encoded correctly"
    return unencoded_ampersands_re.sub('&amp;', value)

def add_links(text, trim_url_limit=None, nofollow=False):
    """
    Converts any URLs in text into clickable links. Works on http://, https:// and
    www. links. Links can have trailing punctuation (periods, commas, close-parens)
    and leading punctuation (opening parens) and it'll still do the right thing.

    If trim_url_limit is not None, the URLs in link text will be limited to
    trim_url_limit characters.

    If nofollow is True, the URLs in link text will get a rel="nofollow" attribute.
    """
    trim_url = lambda x, limit=trim_url_limit: limit is not None and (x[:limit] + (len(x) >=limit and '...' or ''))  or x
    words = word_split_re.split(text)
    nofollow_attr = nofollow and ' rel="nofollow"' or ''
    for i, word in enumerate(words):
        match = punctuation_re.match(word)
        if match:
            lead, middle, trail = match.groups()
            if middle.startswith('www.') or ('@' not in middle and not middle.startswith('http://') and \
                    len(middle) > 0 and middle[0] in string.letters + string.digits and \
                    (middle.endswith('.org') or middle.endswith('.net') or middle.endswith('.com'))):
                middle = '<a href="http://%s"%s>%s</a>' % (middle, nofollow_attr, trim_url(middle))
            if middle.startswith('http://') or middle.startswith('https://'):
                middle = '<a href="%s"%s>%s</a>' % (middle, nofollow_attr, trim_url(middle))
            if '@' in middle and not middle.startswith('www.') and not ':' in middle \
              and simple_email_re.match(middle):
                middle = '<a href="mailto:%s">%s</a>' % (middle, middle)
            if lead + middle + trail != word:
                words[i] = lead + middle + trail
    return ''.join(words)

urlize = add_links

def clean_html(text):
    """
    Cleans the given HTML. Specifically, it does the following:
        * Converts <b> and <i> to <strong> and <em>.
        * Encodes all ampersands correctly.
        * Removes all "target" attributes from <a> tags.
        * Removes extraneous HTML, such as presentational tags that open and
          immediately close and <br clear="all">.
        * Converts hard-coded bullets into HTML unordered lists.
        * Removes stuff like "<p>&nbsp;&nbsp;</p>", but only if it's at the
          bottom of the text.
    """
    from text import normalize_newlines
    text = normalize_newlines(text)
    text = re.sub(r'<(/?)\s*b\s*>', '<\\1strong>', text)
    text = re.sub(r'<(/?)\s*i\s*>', '<\\1em>', text)
    text = fix_ampersands(text)
    # Remove all target="" attributes from <a> tags.
    text = link_target_attribute_re.sub('\\1', text)
    # Trim stupid HTML such as <br clear="all">.
    text = html_gunk_re.sub('', text)
    # Convert hard-coded bullets into HTML unordered lists.
    def replace_p_tags(match):
        s = match.group().replace('</p>', '</li>')
        for d in DOTS:
            s = s.replace('<p>%s' % d, '<li>')
        return '<ul>\n%s\n</ul>' % s
    text = hard_coded_bullets_re.sub(replace_p_tags, text)
    # Remove stuff like "<p>&nbsp;&nbsp;</p>", but only if it's at the bottom of the text.
    text = trailing_empty_content_re.sub('', text)
    return text

# This pattern matches a character entity reference (a decimal numeric
# references, a hexadecimal numeric reference, or a named reference).
charrefpat = re.compile(r'&(#(\d+|x[\da-fA-F]+)|[\w.:-]+);?')

def decode_html(html):
    """
    >>> decode_html('me &amp; you and &#36;&#38;%')
    u'me & you and $&%'
    >>> decode_html('&#x80;')
    u'\u20ac'
    >>> decode_html('Anniversary of Daoud&apos;s Republic')
    u"Anniversary of Daoud's Republic"
    """
    if isinstance(html, bytes):
        html = html.decode('utf-8')
    uchr = unichr
    def entitydecode(match, uchr=uchr):
        entity = match.group(1)
        if entity == '#x80':
            return u'€'
        elif entity.startswith('#x'):
            return uchr(int(entity[2:], 16))
        elif entity.startswith('#'):
            return uchr(int(entity[1:]))
        elif entity in name2codepoint:
            return uchr(name2codepoint[entity])
        elif entity == 'apos':
            return "'"
        else:
            return match.group(0)
    return charrefpat.sub(entitydecode, html).replace(u'\xa0', ' ')

def highlight(text, query, hlClass="hl"):
    """
    >>> highlight('me &amp; you and &#36;&#38;%', 'and')
    'me &amp; you <span class="hl">and</span> &#36;&#38;%'
    """
    if query:
        text = text.replace('<br />', '|')
        query = re.escape(query).replace('\ ', '.')
        m = re.compile("(%s)" % query, re.IGNORECASE).findall(text)
        for i in m:
            text = re.sub("(%s)" % re.escape(i).replace('\ ', '.'), '<span class="%s">\\1</span>' % hlClass, text)
        text = text.replace('|', '<br />')
    return text

def escape_html(value):
    '''
    >>> escape_html(u'<script> foo')
    u'&lt;script&gt; foo'
    >>> escape_html(u'&lt;script&gt; foo')
    u'&lt;script&gt; foo'
    '''
    return escape(decode_html(value))

def sanitize_html(html, tags=None, global_attributes=[]):
    '''
    >>> sanitize_html('http://foo.com, bar')
    u'<a href="http://foo.com">http://foo.com</a>, bar'
    >>> sanitize_html('http://foo.com/foobar?foo, bar')
    u'<a href="http://foo.com/foobar?foo">http://foo.com/foobar?foo</a>, bar'
    >>> sanitize_html('(see: www.foo.com)')
    u'(see: <a href="http://www.foo.com">www.foo.com</a>)'
    >>> sanitize_html('foo@bar.com')
    u'<a href="mailto:foo@bar.com">foo@bar.com</a>'
    >>> sanitize_html(sanitize_html('foo@bar.com'))
    u'<a href="mailto:foo@bar.com">foo@bar.com</a>'
    >>> sanitize_html('<a href="http://foo.com" onmouseover="alert()">foo</a>')
    u'<a href="http://foo.com">foo</a>'
    >>> sanitize_html('<a href="javascript:alert()">foo</a>')
    u'&lt;a href="javascript:alert()"&gt;foo'
    >>> sanitize_html('[http://foo.com foo]')
    u'<a href="http://foo.com">foo</a>'
    >>> sanitize_html('<div style="direction: rtl">foo</div>')
    u'<div style="direction: rtl">foo</div>'
    >>> sanitize_html('<script>alert()</script>')
    u'&lt;script&gt;alert()&lt;/script&gt;'
    >>> sanitize_html("'foo' < 'bar' && \"foo\" > \"bar\"")
    u'\'foo\' &lt; \'bar\' &amp;&amp; "foo" &gt; "bar"'
    >>> sanitize_html('<b>foo')
    u'<b>foo</b>'
    >>> sanitize_html('<b>foo</b></b>')
    u'<b>foo</b>'
    >>> sanitize_html('Anniversary of Daoud&apos;s Republic')
    u"Anniversary of Daoud's Republic"
    '''
    if not tags:
        valid_url = '^((https?:\/\/|\/|mailto:).*?)'
        tags = [
            # inline formatting
            {'name': 'b'},
            {'name': 'bdi'},
            {'name': 'code'},
            {'name': 'em'},
            {'name': 'i'},
            {'name': 'q'},
            {'name': 's'},
            {'name': 'span'},
            {'name': 'strong'},
            {'name': 'sub'},
            {'name': 'sup'},
            {'name': 'u'},
            # block formatting
            {'name': 'blockquote'},
            {'name': 'cite'},
            {
                'name': 'div',
                'optional': ['style'],
                'validation': {
                    'style': '^direction: rtl$'
                }
            },
            {'name': 'h1'},
            {'name': 'h2'},
            {'name': 'h3'},
            {'name': 'h4'},
            {'name': 'h5'},
            {'name': 'h6'},
            {'name': 'p'},
            {'name': 'pre'},
            # lists
            {'name': 'li'},
            {'name': 'ol'},
            {'name': 'ul'},
            # tables
            {'name': 'table'},
            {'name': 'tbody'},
            {'name': 'td'},
            {'name': 'tfoot'},
            {'name': 'th'},
            {'name': 'thead'},
            {'name': 'tr'},
            # other
             {'name': '[]'},
            {
                'name': 'a',
                'required': ['href'],
                'validation': {
                    'href': valid_url
                }
            },
            {'name': 'br'},
            {
                'name': 'iframe',
                'optional': ['width', 'height'],
                'required': ['src'],
                'validation': {
                    'width': '^\d+$',
                    'height': '^\d+$',
                    'src': valid_url
                }
            },
            {
                'name': 'img',
                'optional': ['width', 'height'],
                'required': ['src'],
                'validation': {
                    'width': '^\d+$',
                    'height': '^\d+$',
                    'src': valid_url
                },
            },
            {'name': 'figure'},
            {'name': 'figcaption'}
        ]

    tag_re = re.compile('<(/)?([^\ /]+)(.*?)(/)?>')
    attr_re = re.compile('([^=\ ]+)="([^"]+)"')

    escaped = {}
    level = 0
    non_closing_tags = ['img', 'br']
    required_attributes = {}
    validation = {}
    valid_attributes = {}
    valid_tags = set([tag['name'] for tag in tags if tag['name'] != '[]'])

    for tag in tags:
        valid_attributes[tag['name']] = tag.get('required', []) \
                + tag.get('optional', []) \
                + global_attributes
        required_attributes[tag['name']] = tag.get('required', [])
        validation[tag['name']] = tag.get('validation', {})

    if '[]' in validation:
        html = re.sub(
            re.compile('\[((https?:\/\/|\/).+?) (.+?)\]', re.IGNORECASE),
            '<a href="\\1">\\3</a>', html);

    parts = split_tags(html)
    for i, part in enumerate(parts):
        is_tag = i % 2
        if is_tag:
            t = tag_re.findall(part)
            if not t:
                parts[i] = escape_html(decode_html(part))
                continue
            closing, name, attributes, end = t[0]
            closing = closing != ''
            a = attr_re.findall(attributes)
            attrs = dict(a)

            if not closing and not name in non_closing_tags:
                level += 1

            if not attrs and attributes  or name not in valid_tags:
                valid = False
            else:
                valid = True
                for key in set(attrs) - set(valid_attributes[name]):
                    del attrs[key]
                for key in required_attributes[tag['name']]:
                    if not key in attrs:
                        valid = False

            if valid:
                for attr in attrs:
                    if attr in validation[name]:
                        if not re.compile(validation[name][attr]).findall(attrs[attr]):
                            valid = False
                            break

            if valid and closing:
                valid = not escaped.get(level)
            else:
                escaped[level] = not valid
            if closing:
                level -= 1
            if valid:
                parts[i] = '<%s%s%s>' % (
                    ('/' if closing else ''),
                    name,
                    (' ' + ' '.join(['%s="%s"' % (key, attrs[key]) for key, value in a if key in attrs])
                        if not closing and attrs else '')
                )
            else:
                parts[i] = escape_html(decode_html(part))
        else:
            parts[i] = escape_html(decode_html(part))
    html = ''.join(parts)
    html = html.replace('\n\n', '<br/><br/>')
    html = add_links(html)
    return sanitize_fragment(html)

def split_tags(string):
    tags = []
    def collect(match):
        tags.append(match.group(0))
        return '\0'
    strings = re.sub('<[^<>]+>', collect, string).split('\0')
    tags.append('')
    return [item for sublist in zip(strings, tags) for item in sublist][:-1]

def sanitize_fragment(html):
    '''
    #html5lib reorders arguments, so not usable
    import html5lib
    return html5lib.parseFragment(html).toxml().decode('utf-8')
    '''
    if not html:
        return u''
    import lxml.html
    body = lxml.html.document_fromstring(html).find('body')
    html = lxml.html.tostring(body, encoding='utf-8')[6:-7].decode('utf-8')
    if html.startswith('<p>') and html.endswith('</p>'):
        html = html[3:-4]
    return html
