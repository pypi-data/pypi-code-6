# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2008
import math
import re
import unicodedata

ARTICLES = list(set([
    # def sg, def pl, indef sg, indef pl (each m/f/n)
    'der', 'die', 'das', 'ein', 'eine', # de
    'the', 'a', 'an', # en
    'el', 'la', 'lo', 'los', 'las', 'un', 'una', 'unos', 'unas', # es
    'le', "l'", 'la', 'les', 'un', 'une', 'des', # fr
    'il', 'lo', "l'" 'la', '_i', 'gli', 'le', # it
    'de', 'het', 'een', # nl
     'o', 'a', 'os', '_as', 'um', 'uma', '_uns', 'umas' # pt
     # some _disabled because of collisions
]))
# see http://en.wikipedia.org/wiki/List_of_common_Chinese_surnames
# and http://en.wikipedia.org/wiki/List_of_Korean_family_names
ASIAN_NAMES = [
    'chan', 'chang', 'chao',
    'chen', 'cheong', 'cheung',
    'chong', 'choo',
    'chu', 'chun',
    'hou', 'hsieh', 'hsu', 'hu', 'huang',
    'kuo',
    'li', 'liang', 'lin', 'liu',
    '_park',
    'sun', 'sung',
    'tsao',
    'wang', 'Wong',
    'yang', 'yeong', 'yeung'
]
PREFIXES = [
    'al', 'bin', 'da', 'de', 'del', 'dem', 'den', 'der', 'di', 'dos', 'du',
    'e', 'el', 'la', 'san', 'the', 'van', 'vom', 'von', 'y', 'zu'
]
MIDFIXES = ['und']
SUFFIXES = ['ii', 'iii', 'jr', 'jr.', 'ph.d.', 'phd', 'sr', 'sr.']

UA_ALIASES = {
    'browser': {
        'Chrome': '(CriOS|CrMo)',
        'Firefox': '(Fennec|Firebird|Iceweasel|Minefield|Namoroka|Phoenix|SeaMonkey|Shiretoko)',
        'Nokia Browser': '(OviBrowser)'
    },
    'robot': {},
    'system': {
        'BSD': '(FreeBSD|NetBSD|OpenBSD)',
        'Linux': '(CrOS|MeeGo|webOS)',
        'Unix': '(AIX|HP-UX|IRIX|SunOS)'
    }
}
UA_NAMES = {
    'browser': {
        'chromeframe': 'Chrome Frame',
        'FBForIPhone': 'WebKit',
        'Gecko': 'Mozilla',
        'IEMobile': 'Internet Explorer',
        'konqueror': 'Konqueror',
        'Mozilla': 'Netscape',
        'MSIE': 'Internet Explorer',
        'NokiaBrowser': 'Nokia Browser',
        'Trident': 'Internet Explorer'
    },
    'robot': {},
    'system': {
        'BB': 'BlackBerry',
        'CPU OS': 'iOS',
        'iPhone': 'iOS',
        'iPhone OS': 'iOS',
        'J2ME/MIDP': 'Java',
        'Mac_PowerPC': 'Mac OS',
        'Mac_PPC': 'Mac OS',
        'Macintosh': 'Mac OS',
        'PLAYSTATION': 'PlayStation',
        'S': 'Nokia',
        'Series': 'Nokia',
        'Win': 'Windows',
        'Windows Phone OS': 'Windows Phone',
        'X11': 'Linux'
    }
}
UA_REGEXPS = {
    'browser': [
        '(Camino)\/(\d+)',
        '(Chimera)\/(\d+)',
        '(chromeframe)\/(\d+)',
        '(Epiphany)\/(\d+)', # before Chrome, Chromium and Safari
        '(Chromium)\/(\d+)', # before Chrome
        '(Chrome)\/(\d+)',
        '(FBForIPhone)',
        '(Firefox)\/(\d+)',
        '(Galeon)\/(\d+)',
        '(IEMobile)\/(\d+)',
        '(iCab) (\d+)',
        '(iCab)\/(\d+)',
        '(konqueror)\/(\d+)',
        '(Konqueror)\/(\d+)',
        '(Lynx)\/(\d+)',
        '(Netscape)\d?\/(\d+)',
        '(NokiaBrowser)\/(\d+)',
        '(OmniWeb)\/(\d+)',
        '(Opera)\/.+Version\/(\d+)',
        '(OviBrowser)\/(\d+)',
        'Version\/(\d+).+(Safari)',
        '(WebKit)\/(\d+)',
        '(MSIE) (\d\d?(?!\d))', # last, since Opera used to mask as MSIE
        '(Trident)\/.*?rv:(\d+)',
        '(Gecko)',
        '(Mozilla)\/(3|4)'
    ],
    'robot': [
        '(BingPreview)\/(\d+)',
        '(Google Web Preview).+Chrome\/(\d+)',
        '(Googlebot)\/(\d+)',
        '(WebCrawler)\/(\d+)',
        '(Yahoo! Slurp)\/(\d+)'
    ],
    'system': [
        '(Android) (\d+)',
        '(Android)',
        '(BB)(\d+)',
        '(BeOS)',
        '(BlackBerry) (\d+)',
        '(BlackBerry)',
        '(Darwin)',
        '(BSD) (FreeBSD|NetBSD|OpenBSD)',
        '(CPU OS) (\d+)',
        '(iPhone OS) (\d+)',
        '(iPhone)', # Opera
        '(J2ME\/MIDP)',
        '(Linux).+(CentOS|CrOS|Debian|Fedora|Gentoo|Mandriva|MeeGo|Mint|Red Hat|SUSE|Ubuntu|webOS)',
        '(CentOS|CrOS|Debian|Fedora|Gentoo|Mandriva|MeeGo|Mint|Red Hat|SUSE|Ubuntu|webOS).+(Linux)',
        '(Linux)',
        '(Mac OS X) (10.\d+)',
        '(Mac OS X)',
        '(Mac_PowerPC)',
        '(Mac_PPC)',
        '(Macintosh)',
        'Nintendo (Wii).+NX\/(\d+)',
        '(PLAYSTATION) (\d+)',
        '(PlayStation) Vita (\d+)',
        '(RIM Tablet OS) (\d+)',
        '(S)(60);',
        '(Series) ?(40|60)',
        '(Symbian OS)',
        '(SymbianOS)\/(\d+)',
        '(SymbOS)',
        '(OS\/2)',
        '(Unix) (AIX|HP-UX|IRIX|SunOS)',
        '(Unix)',
        '(Windows) (NT \d\.\d)',
        '(Windows Phone) (\d+)',
        '(Windows Phone OS) (\d+)',
        '(Windows) (3\.1|95|98|2000|2003|CE|ME|Mobile|NT|XP)', # Opera
        '(Win) (9x 4\.90)', # Firefox
        '(Win)(16)', # Firefox
        '(Win)(9\d)', # Firefox
        '(Win)(NT)', # Firefox
        '(Win)(NT4\.0)', # Firefox
        '(X11)'
    ]
}
UA_VERSIONS = {
    'browser': {},
    'robot': {},
    'system': {
        '10.0': '10.0 (Cheetah)',
        '10.1': '10.1 (Puma)',
        '10.2': '10.2 (Jaguar)',
        '10.3': '10.3 (Panther)',
        '10.4': '10.4 (Tiger)',
        '10.5': '10.5 (Leopard)',
        '10.6': '10.6 (Snow Leopard)',
        '10.7': '10.7 (Lion)',
        '10.8': '10.8 (Mountain Lion)',
        '10.9': '10.9 (Mavericks)',
        '10.10': '10.10 (Yosemite)',
        '40': 'Series 40',
        '60': 'Series 60',
        'NT 3.1': 'NT 3.1 (3.1)',
        'NT 3.5': 'NT 3.5 (NT)',
        'NT 4.0': 'NT 4.0 (NT)',
        'NT 4.1': 'NT 4.1 (98)',
        '9x 4.90': 'NT 4.9 (ME)',
        'NT 5.0': 'NT 5.0 (2000)',
        'NT 5.1': 'NT 5.1 (XP)',
        'NT 5.2': 'NT 5.2 (2003)',
        'NT 6.0': 'NT 6.0 (Vista)',
        'NT 6.1': 'NT 6.1 (7)',
        'NT 6.2': 'NT 6.2 (8)',
        'NT 6.3': 'NT 6.3 (8.1)',
        '16': 'NT 3.1 (3.1)',
        '3.1': 'NT 3.1 (3.1)',
        '95': 'NT 4.0 (95)',
        'NT': 'NT 4.0 (NT)',
        'NT4.0': 'NT 4.0 (NT)',
        '98': 'NT 4.1 (98)',
        'ME': 'NT 4.9 (ME)',
        '2000': 'NT 5.0 (2000)',
        'XP': 'NT 5.1 (XP)',
        '2003': 'NT 5.2 (2003)'
    }
}

def get_sort_name(name):
    """

    >>> get_sort_name('Alfred Hitchcock')
    'Hitchcock, Alfred'

    >>> get_sort_name('Jean-Luc Godard')
    'Godard, Jean-Luc'

    >>> get_sort_name('Rainer Werner Fassbinder')
    'Fassbinder, Rainer Werner'

    >>> get_sort_name('Brian De Palma')
    'De Palma, Brian'

    >>> get_sort_name('Johan van der Keuken')
    'van der Keuken, Johan'

    >>> get_sort_name('Edward D. Wood Jr.')
    'Wood Jr., Edward D.'

    >>> get_sort_name('Bing Wang')
    'Wang Bing'

    >>> get_sort_name('Frank Capra III')
    'Capra III, Frank'

    >>> get_sort_name('The Queen of England')
    'Queen of England, The'

    >>> get_sort_name('Sham 69')
    'Sham 69'

    >>> get_sort_name('Scorsese, Martin')
    'Scorsese, Martin'
    """
    if not ' ' in name or ', ' in name:
        return name
    if name.lower().startswith('the '):
        return get_sort_title(name)
    def add_name():
        if len(first_names):
            last_names.insert(0, first_names.pop())
    def find_name(names):
        return len(first_names) and first_names[-1].lower() in names
    first_names = name.split(' ')
    last_names = []
    if re.search('^[0-9]+$', first_names[-1]):
        add_name()
    if find_name(SUFFIXES):
        add_name()
    add_name()
    if find_name(MIDFIXES):
        add_name()
        add_name()
    while find_name(PREFIXES):
        add_name()
    name = ' '.join(last_names)
    if len(first_names):
        separator = ' ' if last_names[0].lower() in ASIAN_NAMES else ', '
        name += separator + ' '.join(first_names)
    return name

def get_sort_title(title):
    """

    >>> get_sort_title('Themroc')
    'Themroc'

    >>> get_sort_title('Die Hard')
    'Hard, Die'

    >>> get_sort_title("L'atalante")
    "atalante, L'"

    """
    for article in ARTICLES:
        spaces = 0 if article.endswith("'") else 1
        if title.lower().startswith(article + ' ' * spaces):
            length = len(article)
            return title[length + spaces:] + ', ' + title[:length]
    return title

def find_re(string, regexp):
    result = re.compile(regexp, re.DOTALL).findall(string)
    if result:
        return result[0].strip()
    return ''

def find_string(string, string0='', string1 = ''):
    """Return the string between string0 and string1. 

    If string0 or string1 is left out, begining or end of string is used.

    >>> find_string('i am not there', string1=' not there')
    'i am'

    >>> find_string('i am not there', 'i am ', ' there')
    'not'

    >>> find_string('i am not there', 'i am not t')
    'here'

    """
    if string0:
        string0 = re.escape(string0)
    else:
        string0 = '^'
    if string1:
        string1 = re.escape(string1)
    else:
        string1 = '$'
    return find_re(string, string0 + '(.*?)' + string1)

def parse_useragent(useragent):
    data = {}
    for key in UA_REGEXPS:
        for alias, regexp in UA_ALIASES[key].items():
            alias = alias if key == 'browser' else alias + ' \\1'
            useragent = re.sub(regexp, alias, useragent)                    
        for regexp in UA_REGEXPS[key]:
            data[key] = {'name': '', 'version': '', 'string': ''}
            match = re.compile(regexp).search(useragent)
            if match:
                matches = list(match.groups())
                if len(matches) == 1:
                    matches.append('')
                swap = re.match('^\d', matches[0]) or matches[1] == 'Linux'
                name = matches[1 if swap else 0]
                version = matches[0 if swap else 1].replace('_', '.')
                name = UA_NAMES[key][name] if name in UA_NAMES[key] else name
                version = UA_VERSIONS[key][version] if version in UA_VERSIONS[key] else version
                string = name
                if version:
                    string = string + ' ' + (
                        '(' + version + ')' if name in ['BSD', 'Linux', 'Unix'] else version
                    )
                data[key] = {
                    'name': name,
                    'version': version,
                    'string': string
                }
                break;
    return data

def remove_special_characters(text):
    """
    Removes special characters inserted by Word.
    """
    text = text.replace(u'\u2013', '-')
    text = text.replace(u'\u2026O', "'")
    text = text.replace(u'\u2019', "'")
    text = text.replace(u'', "'")
    text = text.replace(u'', "'")
    text = text.replace(u'', "-")
    return text

def wrap(text, width):
    """
    A word-wrap function that preserves existing line breaks and most spaces in
    the text. Expects that existing line breaks are posix newlines (\n).
    See http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/148061
    """
    return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                    ' \n'[(len(line[line.rfind('\n')+1:])
                          + len(word.split('\n',1)[0]
                              ) >= width)],
                    word),
                  text.split(' ')
                  )

def wrap_string(string, length=80, separator='\n', balance=False):
    '''
    >>> wrap_string(u"Anticonstitutionellement, Paris s'eveille", 16)
    u"Anticonstitution\\nellement, Paris \\ns'eveille"
    >>> wrap_string(u'All you can eat', 12, '\\n', True)
    u'All you \\ncan eat'
    '''
    words = string.split(' ')
    if balance:
        # balance lines: test if same number of lines
        # can be achieved with a shorter line length
        lines = wrap_string(string, length, separator, False).split(separator)
        if len(lines) > 1:
            while length > max([len(x) for x in words]):
                length -= 1
                if len(wrap_string(string, length, separator, False).split(separator)) > len(lines):
                    length += 1
                    break
    lines = ['']
    for word in words:
        if len(lines[len(lines) - 1] + word + u' ') <= length + 1:
            # word fits in current line
            lines[len(lines) - 1] += word + u' ';
        else:
            if len(word) <= length:
                # word fits in next line
                lines.append(word + u' ')
            else:
                # word is longer than line
                position = length - len(lines[len(lines) - 1])
                lines[len(lines) - 1] += word[0:position]
                for i in range(position, len(word), length):
                    lines.append(word[i:i+length]);
                lines[len(lines) - 1] += u' '
    return separator.join(lines).strip()

def truncate_string(string, length, padding='...', position='right'):
    #  >>> truncate_string('anticonstitutionellement', 16, '...', 'left')
    #  '...utionellement'
    #  >>> truncate_string('anticonstitutionellement', 16, '...', 'center')
    #  'anticon...lement'
    #  >>> truncate_string('anticonstitutionellement', 16, '...', 'right')
    #  'anticonstitut...'
    stringLength = len(string);
    paddingLength = len(padding)
    if stringLength > length:
        if position == 'left':
            string = '%s%s' % (padding, string[stringLength + paddingLength - length:])
        elif position == 'center':
            left = int(math.ceil(float(length - paddingLength) / 2))
            right = int(stringLength - math.floor(float(length - paddingLength) / 2))
            string = '%s%s%s' % (string[:left], padding, string[right:])
        elif position == 'right':
            string = '%s%s' % (string[:length - paddingLength], padding)
    return string;

def truncate_words(s, num):
    """Truncates a string after a certain number of chacters, but ends with a word

    >>> truncate_words('Truncates a string after a certain number of chacters, but ends with a word', 23)
    'Truncates a string...'
    >>> truncate_words('Truncates a string', 23)
    'Truncates a string'

    """
    length = int(num)
    if len(s) <= length:
        return s
    words = s.split()
    ts = ""
    while words and len(ts) + len(words[0]) < length:
        ts += " " + words.pop(0)
    if words:
        ts += "..."
    return ts.strip()

def trim_string(string, num):
    """Truncates a string after a certain number of chacters, adding ... at -10 characters

    >>> trim_string('Truncates a string after a certain number of chacters', 23)
    'Truncates ...f chacters'
    >>> trim_string('Truncates a string', 23)
    'Truncates a string'
    """
    if len(string) > num:
        string = string[:num - 13] + '...' + string[-10:]
    return string

def get_valid_filename(s):
    """
    Returns the given string converted to a string that can be used for a clean
    filename. Specifically, leading and trailing spaces are removed; 
    all non-filename-safe characters are removed.

    >>> get_valid_filename("john's portrait in 2004.jpg")
    'john_s_portrait_in_2004.jpg'
    """
    s = s.strip()
    s = s.replace(' ', '_')
    s = re.sub(r'[^-A-Za-z0-9_.\[\]\ ]', '_', s)
    s = s.replace('__', '_').replace('__', '_')
    return s

def get_text_list(list_, last_word='or'):
    """
    >>> get_text_list([u'a', u'b', u'c', u'd'])
    u'a, b, c or d'
    >>> get_text_list([u'a', u'b', u'c'], 'and')
    u'a, b and c'
    >>> get_text_list([u'a', u'b'], 'and')
    u'a and b'
    >>> get_text_list([u'a'])
    u'a'
    >>> get_text_list([])
    ''
    """
    if len(list_) == 0: return ''
    if len(list_) == 1: return list_[0]
    return u'%s %s %s' % (u', '.join([unicode(i) for i in list_][:-1]), last_word, list_[-1])

def get_list_text(text, last_word='or'):
    """
    >>> get_list_text(u'a, b, c or d')
    [u'a', u'b', u'c', u'd']
    >>> get_list_text(u'a, b and c', u'and')
    [u'a', u'b', u'c']
    >>> get_list_text(u'a and b', u'and')
    [u'a', u'b']
    >>> get_list_text(u'a')
    [u'a']
    >>> get_list_text(u'')
    []
    """
    list_ = []
    if text:
        list_ = text.split(u', ')
        if list_:
            i=len(list_)-1
            last = list_[i].split(last_word)
            if len(last) == 2:
                list_[i] = last[0].strip()
                list_.append(last[1].strip())
    return list_

def normalize_newlines(text):
    return re.sub(r'\r\n|\r|\n', '\n', text)

def recapitalize(text):
    "Recapitalizes text, placing caps after end-of-sentence punctuation."
    #capwords = ()
    text = text.lower()
    capsRE = re.compile(r'(?:^|(?<=[\.\?\!] ))([a-z])')
    text = capsRE.sub(lambda x: x.group(1).upper(), text)
    #for capword in capwords:
    #    capwordRE = re.compile(r'\b%s\b' % capword, re.I)
    #    text = capwordRE.sub(capword, text)
    return text

def phone2numeric(phone):
    "Converts a phone number with letters into its numeric equivalent."
    letters = re.compile(r'[A-PR-Y]', re.I)
    char2number = lambda m: {'a': '2', 'c': '2', 'b': '2', 'e': '3',
          'd': '3', 'g': '4', 'f': '3', 'i': '4', 'h': '4', 'k': '5',
          'j': '5', 'm': '6', 'l': '5', 'o': '6', 'n': '6', 'p': '7',
          's': '7', 'r': '7', 'u': '8', 't': '8', 'w': '9', 'v': '8',
          'y': '9', 'x': '9'}.get(m.group(0).lower())
    return letters.sub(char2number, phone)

def compress_string(s):
    import cStringIO, gzip
    zbuf = cStringIO.StringIO()
    zfile = gzip.GzipFile(mode='wb', compresslevel=6, fileobj=zbuf)
    zfile.write(s)
    zfile.close()
    return zbuf.getvalue()

smart_split_re = re.compile('("(?:[^"\\\\]*(?:\\\\.[^"\\\\]*)*)"|\'(?:[^\'\\\\]*(?:\\\\.[^\'\\\\]*)*)\'|[^\\s]+)')
def smart_split(text):
    """
    Generator that splits a string by spaces, leaving quoted phrases together.
    Supports both single and double quotes, and supports escaping quotes with
    backslashes. In the output, strings will keep their initial and trailing
    quote marks.
    >>> list(smart_split('This is "a person\\'s" test.'))
    ['This', 'is', '"a person\\'s"', 'test.']
    """
    for bit in smart_split_re.finditer(text):
        bit = bit.group(0)
        if bit[0] == '"':
            yield '"' + bit[1:-1].replace('\\"', '"').replace('\\\\', '\\') + '"'
        elif bit[0] == "'":
            yield "'" + bit[1:-1].replace("\\'", "'").replace("\\\\", "\\") + "'"
        else:
            yield bit

def words(text):
    """
        returns words in text, removing punctuation
    """
    text = text.split()
    return map(lambda x: re.sub("(([.!?:-_]|'s)$)", '', x), text)

def sort_string(string):
    string = string.replace(u'Æ', 'AE').replace(u'Ø', 'O').replace(u'Þ', 'Th')

    #pad numbered titles
    string = re.sub('(\d),(\d{3})', '\\1\\2', string)
    string = re.sub('(\d+)', lambda x: '%010d' % int(x.group(0)), string)
    return unicodedata.normalize('NFKD', string)

def sorted_strings(strings, key=None):
    if not key:
        key = lambda k: sort_string(k)
    return sorted(strings, key=key)
