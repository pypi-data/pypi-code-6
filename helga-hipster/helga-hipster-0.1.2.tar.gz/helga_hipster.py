import random
import urllib

import requests

from helga import settings
from helga.plugins import command


ENDPOINT = 'http://developer.echonest.com/api/v4/song/search'

BASE_PARAMS = {
    'format': 'json',
    'results': '1',
    'bucket': 'id:spotify'
}

RESPONSES = [
    u"You've probably never heard of them, but you should check out {thing}",
    u"I'm going to stop listening to {thing} once it goes mainstream",
    u"{thing} is probably the best thing you've never listened to",
    u"{thing} is great, but you you've probably never heard of it",
]


STYLES = None


def get_all_styles(api_key):
    global STYLES

    url = u'http://developer.echonest.com/api/v4/artist/list_terms?api_key={key}&format=json&type=style'
    data = requests.get(url.format(key=api_key)).json()

    STYLES = [t['name'] for t in data['response']['terms']]


def fetch_song(api_key, style=None):
    global ENDPOINT, BASE_PARAMS

    params = BASE_PARAMS.copy()
    params['api_key'] = api_key

    min_lat = random.randint(-900, 900) / 10.0
    max_lat = random.randint(min_lat * 10, 900) / 10.0
    min_long = random.randint(-1800, 1800) / 10.0
    max_long = random.randint(min_long * 10, 1800) / 10.0

    params.update({
        'min_latitude': min_lat,
        'max_latitude': max_lat,
        'min_longitude': min_long,
        'max_longitude': max_long,
        'artist_max_hotttnesss': '0.3',
    })

    if style:
        params['style'] = style

    url = '{0}?{1}&bucket=tracks'.format(ENDPOINT, urllib.urlencode(params))
    resp = requests.get(url)
    resp.raise_for_status()

    data = resp.json()

    try:
        return random.choice(data['response']['songs'])
    except IndexError:
        return fetch_song(api_key)


@command('hipster', help='Hipster music. Useage: helga hipster')
def hipster(client, channel, nick, message, cmd, args):
    global RESPONSES, STYLES

    api_key = getattr(settings, 'HIPSTER_ECHONEST_API_KEY', None)
    if not api_key:
        return u"It doesn't look like I'm configured correctly {nick}".format(nick=nick)

    if STYLES is None:
        get_all_styles(api_key)

    style = random.choice(STYLES) if STYLES else None

    song = fetch_song(api_key, style)
    thing = u"'{track}' by {artist}".format(track=song['title'], artist=song['artist_name'])

    if song['tracks']:
        spotify = song['tracks'][0]['foreign_id']
        _, _, spotify_id = spotify.split(':')
        spotify_url = u'http://open.spotify.com/track/{0}'.format(spotify_id)

        thing = u"'{track}' by {artist} ({url})".format(track=song['title'],
                                                        artist=song['artist_name'],
                                                        url=spotify_url)

    msg = random.choice(RESPONSES).format(thing=thing)

    if style:
        msg = u'[{style}] {msg}'.format(style=style, msg=msg)

    return msg
