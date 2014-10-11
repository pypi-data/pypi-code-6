# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2008
import re
import unicodedata

_articles = ('the', 'la', 'a', 'die', 'der', 'le', 'el',
             "l'", 'il', 'das', 'les', 'o', 'ein', 'i', 'un', 'los', 'de',
             'an', 'una', 'las', 'eine', 'den', 'gli', 'het', 'os', 'lo',
             'az', 'det', 'ha-', 'een', 'ang', 'oi', 'ta', 'al-', 'dem',
             'mga', 'uno', "un'", 'ett', u'\xcf', 'eines', u'\xc7', 'els',
             u'\xd4\xef', u'\xcf\xe9')

# Articles in a dictionary.
_articlesDict = dict([(x, x) for x in _articles])
_spArticles = []
for article in _articles:
    if article[-1] not in ("'", '-'): article += ' '
    _spArticles.append(article)

_noarticles = (
    'los angeles',
    'i am ',
    'i be area',
    'i call ',
    'i come ',
    'i confess',
    'i hired ',
    'i killed ',
    'i know ',
    'i live ',
    'i love',
    'i married',
    'i never',
    'i shot',
    'i start',
    'i was',
)

def canonical_title(title):
    """Return the title in the canonic format 'Movie Title, The'.
    
    >>> canonical_title('The Movie Title')
    'Movie Title, The'

    >>> canonical_title('Los Angeles Plays Itself')
    'Los Angeles Plays Itself'
    """
    try:
        if _articlesDict.has_key(title.split(', ')[-1].lower()): return title
    except IndexError: pass
    ltitle = title.lower()
    for start in _noarticles:
        if ltitle.startswith(start):
            return title
    for article in _spArticles:
        if ltitle.startswith(article):
            lart = len(article)
            title = '%s, %s' % (title[lart:], title[:lart])
            if article[-1] == ' ': title = title[:-1]
            break
    ## XXX: an attempt using a dictionary lookup.
    ##for artSeparator in (' ', "'", '-'):
    ##    article = _articlesDict.get(ltitle.split(artSeparator)[0])
    ##    if article is not None:
    ##        lart = len(article)
    ##        # check titles like "una", "I'm Mad" and "L'abbacchio".
    ##        if title[lart:] == '' or (artSeparator != ' ' and
    ##                                title[lart:][1] != artSeparator): continue
    ##        title = '%s, %s' % (title[lart:], title[:lart])
    ##        if artSeparator == ' ': title = title[1:]
    ##        break
    return title

def normalize_title(title):
    """Return the title in the normal "The Title" format.

    >>> normalize_title('Movie Title, The')
    'The Movie Title'
    """
    stitle = title.split(', ')
    if len(stitle) > 1 and _articlesDict.has_key(stitle[-1].lower()):
        sep = ' '
        if stitle[-1][-1] in ("'", '-'): sep = ''
        title = '%s%s%s' % (stitle[-1], sep, ', '.join(stitle[:-1]))
    return title

def normalize_imdbid(imdbId):
    """Return 7 digit imdbId.

    >>> normalize_imdbid('http://www.imdb.com/title/tt0159206/')
    '0159206'
    >>> normalize_imdbid(159206)
    '0159206'
    >>> normalize_imdbid('tt0159206')
    '0159206'
    """
    if isinstance(imdbId, basestring):
        imdbId = re.sub('.*(\d{7}).*', '\\1', imdbId)
    elif isinstance(imdbId, int):
        imdbId = "%07d" % imdbId
    return imdbId


# Common suffixes in surnames.
_sname_suffixes = (
    'al', 'ben', 'da', 'de', 'del', 'den', 'der', 'des', 'di', 'dos', 'du',
    'e', 'el', 'la', 'le', 'the', 'vom', 'von', 'van', 'y'
)

def canonical_name(name):
    """Return the given name in canonical "Surname, Name" format.
    It assumes that name is in the 'Name Surname' format.
    
    >>> canonical_name('Jean Luc Godard')
    'Godard, Jean Luc'

    >>> canonical_name('Ivan Ivanov-Vano')
    'Ivanov-Vano, Ivan'

    >>> canonical_name('Gus Van Sant')
    'Van Sant, Gus'

    >>> canonical_name('Brian De Palma')
    'De Palma, Brian'
    """

    # XXX: some statistics (over 1852406 names):
    #      - just a surname:                 51921
    #      - single surname, single name:  1792759
    #      - composed surname, composed name: 7726
    #      - composed surname, single name:  55623
    #        (2: 49259, 3: 5502, 4: 551)
    #      - single surname, composed name: 186604
    #        (2: 178315, 3: 6573, 4: 1219, 5: 352)
    # Don't convert names already in the canonical format.
    if name in ('Unknown Director', ):
        return name
    if name.find(', ') != -1: return name
    sname = name.split(' ')
    snl = len(sname)
    if snl == 2:
        # Just a name and a surname: how boring...
        name = '%s, %s' % (sname[1], sname[0])
    elif snl > 2:
        lsname = [x.lower() for x in sname]
        if snl == 3: _indexes = (0, snl-2)
        else: _indexes = (0, snl-2, snl-3)
        # Check for common surname prefixes at the beginning and near the end.
        for index in _indexes:
            if lsname[index] not in _sname_suffixes: continue
            try:
                # Build the surname.
                surn = '%s %s' % (sname[index], sname[index+1])
                del sname[index]
                del sname[index]
                try:
                    # Handle the "Jr." after the name.
                    if lsname[index+2].startswith('jr'):
                        surn += ' %s' % sname[index]
                        del sname[index]
                except (IndexError, ValueError):
                    pass
                name = '%s, %s' % (surn, ' '.join(sname))
                break
            except ValueError:
                continue
        else:
            name = '%s, %s' % (sname[-1], ' '.join(sname[:-1]))
    return name

def normalize_name(name):
    """Return a name in the normal "Name Surname" format.
    
    >>> normalize_name('Godard, Jean Luc')
    'Jean Luc Godard'

    >>> normalize_name('Ivanov-Vano, Ivan')
    'Ivan Ivanov-Vano'

    >>> normalize_name('Van Sant, Gus')
    'Gus Van Sant'

    >>> normalize_name('De Palma, Brian')
    'Brian De Palma'
    """
    sname = name.split(', ')
    if len(sname) == 2:
        name = '%s %s' % (sname[1], sname[0])
    return name

def normalize_path(path):
    path = path.replace(':', '_').replace('/', '_')
    if path.endswith('.'): path = path[:-1] + '_'
    return path

def strip_accents(s):
    if isinstance(s, str):
        s = unicode(s)
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

