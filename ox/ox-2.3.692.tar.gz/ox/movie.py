# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2012

from __future__ import division

import hashlib 
import os
import re
import unicodedata

from .normalize import normalize_name
from .text import get_sort_name, find_re
from .file import EXTENSIONS

__all__ = ['parse_movie_path', 'create_movie_path', 'get_oxid']

LANGUAGES = ['en', 'fr', 'de', 'es', 'it']

'''
Naming scheme:
X/[Group, The; Lastname, Firstname/]The Title[ (YEAR[-[YEAR]])]/
The Title[ ([SXX][EYY[+ZZ|-ZZ]])[ Episode Title]][.Version][.Part XY[.Part Title][.en][.fr].xyz
'''

def format_path(data, directory_key='director'):
    def format_underscores(string):
        return re.sub('^\.|\.$|:|/|\?|<|>', '_', string)
    director = data['directorSort'] or ['Unknown Director']
    title = data['seriesTitle' if data['isEpisode'] else 'title'] or 'Untitled'
    year = data['seriesYear' if data['isEpisode'] else 'year'] or None
    parts = map(format_underscores, filter(lambda x: x != None, [
        u'; '.join(director[:10]),
        u'%s%s' % (title, u' (%s)' % year if year else ''),
        u'%s%s%s%s%s%s' % (
            data['title'] or 'Untitled',
            u'.%s' % data['version'] if data['version'] else '',
            u'.Part %s' % data['part'] if data['part'] else '',
            u'.%s' % data['partTitle'] if data['partTitle'] else '',
            u'.%s' % data['language'] if data['language'] else '',
            u'.%s' % data['extension'] if data['extension'] else ''
        )
    ]))
    if data.get('subdirectory'):
        parts.insert(-1, data['subdirectory'])
    return unicodedata.normalize('NFD', u'/'.join(parts))

def parse_item_files(files):
    # parses a list of file objects associated with one item (file objects
    # as returned by parse_path, but extended with 'path' and 'time')
    # and returns a list of version objects (in case of english-only subtitles,
    # version[i]['files'][j]['normalizedPath'] will be modified)
    def get_file_key(file):
        return '\n'.join([
            file['version'] or '',
            file['part'] or '',
            file['language'] or '',
            file['extension'] or ''
        ])
    def get_version_key(file, extension=True):
        return '%s/%s-part/%s' % (
            file['version'] or '',
            'single' if file['part'] == None else 'multi',
            file['extension'] if extension else ''
        )
    # filter out duplicate files (keep shortest path, sorted alphabetically)
    # since same version+part+language+extension can still differ in part title,
    # ''/'en' or 'mpg'/'mpeg', or have an unparsed section in their path
    unique_files = []
    duplicate_files = []
    for key in [get_file_key(file) for file in files]:
        key_files = sorted(
            sorted([file for file in files if get_file_key(file) == key]),
            key=lambda x: len(x['path'])
        )
        unique_files.append(key_files[0])
        duplicate_files += key_files[1:]
    # determine versions ('version.single|multi-part.videoextension')
    version_files = {}
    time = {}
    video_files = [file for file in unique_files if file['type'] == 'video']
    versions = set([file['version'] for file in video_files])
    for version in versions:
        for file in [file for file in video_files if file['version'] == version]:
            version_key = get_version_key(file)
            version_files[version_key] = (version_files[version_key] if version_key in version_files else []) + [file]
            time[version_key] = sorted([time[version_key], file['time']])[-1] if version_key in time else file['time']
    # determine preferred video extension (newest)
    extension = {}
    for key in set(['/'.join(version_key.split('/')[:-1]) + '/' for version_key in version_files]):
        extensions = set([version_key.split('/')[-1] for version_key in version_files if version_key.startswith(key)])
        extension[key] = sorted(extensions, key=lambda x: time[key + x])[-1]
    # associate other (non-video) files
    other_files = [file for file in unique_files if file['type'] != 'video']
    versions = set([file['version'] for file in other_files])
    for version in versions:
        for file in [file for file in other_files if file['version'] == version]:
            key = get_version_key(file, extension=False)
            if key in extension:
                version_files[key + extension[key]].append(file)
            else:
                version_files[key] = (version_files[key] if key in version_files else []) + [file]
                extension[key] = ''
    # determine main files (video + srt)
    full = {}
    language = {}
    main_files = {}
    for version_key in version_files:
        parts = sorted(list(set([file['part'] for file in version_files[version_key]])))
        # determine if all parts have one video file
        video_files = [file for file in version_files[version_key] if file['type'] == 'video']
        full[version_key] = len(video_files) == len(parts)
        main_files[version_key] = video_files if full[version_key] else []
        # determine preferred subtitle language
        language[version_key] = None
        subtitle_files = [file for file in version_files[version_key] if file['extension'] == 'srt']
        for subtitle_language in sorted(
            list(set([file['language'] for file in subtitle_files])),
            key=lambda x: LANGUAGES.index(x) if x in LANGUAGES else x
        ):
            language_files = [file for file in subtitle_files if file['language'] == subtitle_language]
            if len(subtitle_files) == len(parts):
                language[version_key] = subtitle_language
                main_files[version_key] += language_files
                break
    # determine main version (best srt language, then video time)
    main_version = None
    full_version_keys = sorted(
        [version_key for version_key in version_files if full[version_key]],
        key=lambda x: time[x],
        reverse=True
    )
    if full_version_keys:
        language_version_keys = sorted(
            [version_key for version_key in full_version_keys if language[version_key]],
            key=lambda x: LANGUAGES.index(language[x]) if language[x] in LANGUAGES else language[x]
        )
        main_version = language_version_keys[0] if language_version_keys else full_version_keys[0]
    # add duplicate files
    for file in duplicate_files:
        key = get_version_key(file, extension=False)
        version_key = '%s%s' % (key, extension[key] if key in extension else '')
        version_files[version_key] = (version_files[version_key] if version_key in version_files else []) + [file]
    # remove unneeded '.en'
    for version_key in version_files:
        for extension in EXTENSIONS['subtitle']:
            subtitle_files = [file for file in version_files[version_key] if file['extension'] == extension]
            subtitle_languages = list(set([file['language'] for file in subtitle_files]))
            if len(subtitle_languages) == 1 and subtitle_languages[0] == LANGUAGES[0]:
                for subtitle_file in subtitle_files:
                    subtitle_file['normalizedPath'] = format_path(dict(subtitle_file, **{'language': None}))
    # return data
    data = []
    for version_key in version_files:
        data.append({
            'files': sorted(
                [dict(file, isMainFile=file in main_files[version_key]) for file in version_files[version_key]],
                key=lambda x: x['path']
            ),
            'isFullVersion': full[version_key],
            'isMainVersion': version_key == main_version,
            'subtitleLanguage': language[version_key] if version_key in language else None,
            'version': version_key
        })
    return data

def parse_path(path, directory_key='director'):
    '''
    # all keys
    >>> parse_path('Frost, Mark; Lynch, David/Twin Peaks (1991)/Twin Peaks (S01E01) Pilot.European Version.Part 1.Welcome to Twin Peaks.en.fr.MPEG')['normalizedPath']
    'Frost, Mark; Lynch, David/Twin Peaks (1991)/Twin Peaks (S01E00) Pilot.European Version.Part 1.Welcome to Twin Peaks.en.fr.mpg'

    # pop directory title off file name
    >>> parse_path("Unknown Director/www.xxx.com.._/www.xxx.com....Director's Cut.avi")['version']
    "Director's Cut"

    # handle dots
    >>> parse_path("Unknown Director/Unknown Title (2000)/... Mr. .com....Director's Cut.srt")['version']
    "Director's Cut"

    # multiple years, season zero, multiple episodes, dots in episode title and part title
    >>> parse_path('Groening, Matt/The Simpsons (1989-2012)/The Simpsons (S00E01-02) D.I.Y..Uncensored Version.Part 1.D.I.Y..de.avi')['normalizedPath']
    'Groening, Matt/The Simpsons (1989-2012)/The Simpsons (S01E01+02) D.I.Y..Uncensored Version.Part 1.D.I.Y..de.avi'

    # handle underscores
    >>> parse_path('Unknown Director/_com_ 1_0 _ NaN.._/_com_ 1_0 _ NaN....avi')['title']
    '.com: 1/0 / NaN...'

    # TODO: '.com.avi'
    '''
    def parse_title(string):
        return title, year
    def parse_type(string):
        for type in EXTENSIONS:
            if string in EXTENSIONS[type]:
                return type
        return None
    def parse_underscores(string):
        # '^_' or '_$' is '.'
        string = re.sub('^_', '.', string)
        string = re.sub('_$', '.', string)
        # '_.foo$' or '_ (' is '?'
        string = re.sub('_(?=(\.\w+$| \())', '?', string)
        # ' _..._ ' is '<...>'
        string = re.sub('(?<= )_(.+)_(?= )', '<\g<1>>', string)
        # 'foo_bar' or 'foo _ bar' is '/'
        string = re.sub('(?<=\w)_(?=\w)', '/', string)
        string = re.sub(' _ ', ' / ', string)
        # 'foo_ ' is ':'
        string = re.sub('(?<=\w)_ ', ': ', string)
        return string
    data = {}
    parts = map(lambda x: parse_underscores(x.strip()), path.split('/'))
    # subdirectory
    if len(parts) > 4:
        data['subdirectory'] = '/'.join(parts[3:-1])
        parts = parts[:3] + parts[-1:]
    else:
        data['subdirectory'] = None
    length = len(parts)
    director, title, file = [
        parts[-3] if length > 2 else None,
        parts[-2] if length > 1 else None,
        parts[-1]
    ]
    # directorSort, director
    data['directorSort'] = data['director'] = []
    if director:
        data['directorSort'] = filter(
            lambda x: x != 'Unknown Director',
            director.split('; ')
        )
        data['director'] = map(
            lambda x: ' '.join(reversed(x.split(', '))),
            data['directorSort']
        )
    # title, year
    data['title'] = data['year'] = None
    if title:
        match = re.search(' \(\d{4}(-(\d{4})?)?\)$', title)
        data['title'] = title[:-len(match.group(0))] if match else title
        data['year'] = match.group(0)[2:-1] if match else None        
        file_title = re.sub('[/:]', '_', data['title'])
        # (remove title from beginning of filename if the rest contains a dot)
        file = re.sub('^' + re.escape(file_title) + '(?=.*\.)', '', file)
    # (split by nospace+dot+word, but remove spaces preceding extension)
    parts = re.split('(?<!\s)\.(?=\w)', re.sub('\s+(?=.\w+$)', '', file))
    title, parts, extension = [
        parts[0],
        parts[1:-1],
        parts[-1] if len(parts) > 1 else None
    ]
    if not data['title'] and title:
        data['title'] = title
    # season, episode, episodes, episodeTitle
    data['season'] = data['episode'] = data['episodeTitle'] = None
    data['episodes'] = []
    match = re.search(' \((S\d{2})?(E\d{2}([+-]\d{2})?)?\)(.+)?', title)
    if match:
        if match.group(1):
            data['season'] = int(match.group(1)[1:])
        if match.group(2):
            if len(match.group(2)) == 3:
                data['episode'] = int(match.group(2)[1:])
            else:
                data['episodes'] = range(int(match.group(2)[1:3]), int(match.group(2)[-2:]) + 1)
        if match.group(4):
            data['episodeTitle'] = match.group(4)[1:]
    while data['episodeTitle'] and len(parts) and re.search('^\w+\.*$', parts[0]) and not re.search('^[a-z]{2}$', parts[0]):
        data['episodeTitle'] += '.%s' % parts.pop(0)
    # isEpisode, seriesTitle, seriesYear
    data['isEpisode'] = False
    data['seriesTitle'] = data['seriesYear'] = None
    if data['season'] != None or data['episode'] != None or data['episodes']:
        data['isEpisode'] = True
        data['seriesTitle'] = data['title']
        season = 'S%02d' % data['season'] if data['season'] != None else ''
        episode = ''
        if data['episode'] != None:
            episode = 'E%02d' % data['episode']
        elif data['episodes']:
            episode = 'E%02d%s%02d' % (
                data['episodes'][0], '+' if len(data['episodes']) == 2 else '-', data['episodes'][-1]
            )
        episodeTitle = ' %s' % data['episodeTitle'] if data['episodeTitle'] else '' 
        data['title'] += ' (%s%s)%s' % (season, episode, episodeTitle)
        data['seriesYear'] = data['year']
        data['year'] = None
    # version
    data['version'] = parts.pop(0) if len(parts) and re.search('^[A-Z0-9]', parts[0]) and not re.search('^Part .', parts[0]) else None        
    # part
    data['part'] = parts.pop(0)[5:] if len(parts) and re.search('^Part .', parts[0]) else None
    # partTitle
    data['partTitle'] = parts.pop(0) if len(parts) and re.search('^[A-Z0-9]', parts[0]) and data['part'] else None
    while data['partTitle'] and len(parts) and not re.search('^[a-z]{2}$', parts[0]):
        data['partTitle'] += '.%s' % parts.pop(0)
    # language
    data['language'] = parts.pop(0) if len(parts) and re.search('^[a-z]{2}$', parts[0]) else None
    # extension
    data['extension'] = re.sub('^mpeg$', 'mpg', extension.lower()) if extension else None
    # type
    data['type'] = parse_type(data['extension'])
    # normalizedPath
    data['normalizedPath'] = format_path(data)
    return data


def parse_movie_path(path):
    """
        "A/Abrams, J.J.; Lieber, Jeffrey; Lindelof, Damon/Lost (2004)/Lost.Season 3.Episode 21.Greatest Hits.avi"
        "B/Balada, Ivan/Metrum (1967)/Metrum.Part 1.en.srt"
        "N/Nakata, Hideo/L - Change the World (2008)/L - Change the World.Part 2.srt"
        "R/Reitz, Edgar/Heimat (1984-2006)/Heimat.Season 2.Episode 8.The Wedding.Part 2.avi"
        "F/Feuillade, Louis/Les vampires (1915)/Les vampires.Episode 10.Part 2.avi"
            title: 'Les vampires', year: '1915', episode: 10, part: 2

        "G/Godard, Jean-Luc/Histoire(s) du cinema_ Toutes les histoires (1988)/Histoire(s) du cinema_ Toutes les histoires.avi"
        "G/Godard, Jean-Luc/Six fois deux (1976)/Six fois deux.Part 1A.Y a personne.avi"
        "G/Godard, Jean-Luc; Miéville, Anne-Marie/France_tour_detour_deux_enfants (1977)/France_tour_detour_deux_enfants.Part 5.Impression_Dictée.avi"

        "L/Labarthe, André S_/Cinéastes de notre temps (1964-)/Cinéastes de notre temps.Episode.Jean Renoir le patron, première partie_ La Recherche du relatif.avi"
        "S/Scott, Ridley/Blade Runner (1982)/Blade Runner.Directors's Cut.avi"

        or
        
        T/Title (Year)/Title.avi
    """
    episodeTitle = episodeYear = seriesTitle = None
    episodeDirector = []
    parts = path.split('/')

    #title/year
    if len(parts) == 4:
        title = parts[2]
    elif len(parts) > 1:
        title = parts[1]
    else:
        title = parts[0]
    title = title.replace('_ ', ': ')
    if title.endswith('_'):
        title = title[:-1] + '.'
    if title.startswith('_'):
        title = '.' + title[1:]

    year = find_re(title, '(\(\d{4}\))')
    if not year:
        year = find_re(title, '(\(\d{4}-\d*\))')
    if year and title.endswith(year):
        title = title[:-len(year)].strip()
        year = year[1:-1]
        if '-' in year:
            year = find_re(year, '\d{4}')

    #director
    if len(parts) == 4:
        director = parts[1]
        if director.endswith('_'):
            director = "%s." % director[:-1]
        director = director.split('; ')
        director = [normalize_name(d).strip() for d in director]
        director = filter(lambda d: d not in ('Unknown Director', 'Various Directors'), director)
    else:
        director = []

    #extension/language
    fileparts = [x.replace('||', '. ') for x in parts[-1].replace('. ', '||').split('.')]
    extension = len(fileparts) > 1 and fileparts[-1] or ''

    if len(fileparts) > 1 and len(fileparts[-2]) == 2:
        language = fileparts[-2]
    else:
        language = ''
    
    #season/episode/episodeTitle
    match = re.compile('(.+?) \((S(\d+))?(E(\d+))?\)( (.+?))?\.').match(parts[-1])
    if match:
        seriesTitle = match.group(1)
        season = match.group(3)
        episode = match.group(5)
        episodeTitle = (match.group(6) or '').strip()
        if episode != None:
            episode = int(episode)
        if season != None:
            season = int(season)
        if episode and not season:
            season = 1
    else:
        season = find_re(parts[-1], '\.Season (\d+)\.')
        if season:
            season = int(season)
        else:
            season = None

        episode = find_re(parts[-1], '\.Episode[s]* ([\d+]+)\.')
        if episode:
            episode = episode.split('+')[0]
            episode = int(episode)
        else:
            episode = None

        if episode and 'Episode %d'%episode in fileparts:
            episodeTitle = fileparts.index('Episode %d' % episode) + 1
            episodeTitle = fileparts[episodeTitle]
            if episodeTitle == extension or episodeTitle.startswith('Part'):
                episodeTitle = None

        if not season and 'Episode' in fileparts:
            episodeTitle = fileparts.index('Episode') + 1
            episodeTitle = fileparts[episodeTitle]
            if episodeTitle == extension or episodeTitle.startswith('Part'):
                episodeTitle = None
            else:
                season = 1

    if season:
        seriesTitle = title
        title = u'%s (S%02d)' % (seriesTitle, season)
        if isinstance(episode, int):
            title = u'%s (S%02dE%02d)' % (seriesTitle, season, episode)
        if episodeTitle:
            title = u'%s %s' % (title, episodeTitle)

    #part
    part = find_re(parts[-1], '\.Part (\d+)\.')
    if part:
        part = int(part)
    else:
        part = 0

    return {
        'director': director,
        'episodeDirector': episodeDirector,
        'episode': episode,
        'episodeTitle': episodeTitle,
        'episodeYear': episodeYear,
        'extension': extension,
        'language': language,
        'part': part,
        'season': season,
        'seriesTitle': seriesTitle,
        'title': title,
        'year': year,
    }

def create_movie_path(title, director, year,
                      season, episode, episodeTitle, episodeDirector, episodeYear,
                      part, language, extension):
    '''
    {
            title: '', director: [''], year: '',
                    season: int, episode: int, episodeTitle: '', episodeDirector: [''], episodeYear: '',
                            part: int, language: '', extension: '', extra: bool
                                })
    '''
    partTitle = None
    director = '; '.join(map(get_sort_name, director))
    episodeDirector = '; '.join(map(get_sort_name, episodeDirector))
    filename = [title]
    if season:
        filename += ['Season %d' % season]
    if episode:
        filename += ['Episode %d' % episode]
    if episodeTitle:
        filename += [episodeTitle]
    if part:
        filename += ['Part %s' % part]
    if partTitle:
        filename += [partTitle]
    if extension:
        filename += [extension]
    filename = '.'.join(filename)
    path = os.path.join(director[0], director, '%s (%s)' % (title, year), filename)
    return path

def get_oxid(title, director=[], year='',
             season='', episode='', episode_title='', episode_director=[], episode_year=''):
    def get_hash(string):
        return hashlib.sha1(string.encode('utf-8')).hexdigest().upper()
    director = ', '.join(director)
    episode_director = ', '.join(episode_director)
    if not season and not episode and not episode_title:
        oxid = get_hash(director)[:8] + get_hash('\n'.join([title, str(year)]))[:8]
    else:
        oxid = get_hash('\n'.join([director, title, str(year), str(season)]))[:8] + \
               get_hash('\n'.join([str(episode), episode_director, episode_title, str(episode_year)]))[:8]
    return u'0x' + oxid
