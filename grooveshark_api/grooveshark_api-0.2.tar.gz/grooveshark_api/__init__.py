# coding: utf-8

import hmac
import json
import requests
from grooveshark_api.exception import InvalidArgumentValueException, \
    InvalidCredentialsException, RequestErrorException


GROOVESHARK_SSL_ENDPOINT = 'https://api.grooveshark.com/ws3.php'


class Grooveshark(object):

    def __init__(self, key, secret, sessionID=None,
                 user_login=None, user_pass=None):
        self.KEY = key
        self.SECRET = secret
        user = {}
        if sessionID:
            self.sessionID = sessionID
        elif user_login and user_pass:
            self.sessionID = self._get_new_session()
            result = self._establish_session(user_login, user_pass)
            user['name'] = "{0} {1}".format(result.get("FName", None),
                                            result.get("LName", None))
            user['email'] = result.get("Email", None)
            user['login'] = user_login

        self.user = user

    def _request(self, method, params={}, sessionID=False):
        header = {"wsKey": self.KEY}
        if sessionID is True:
            header.update({'sessionID': self.sessionID})

        payload = {"method": method,
                   "parameters": params,
                   "header": header}

        sig = hmac.new(self.SECRET, json.dumps(payload))
        sig = sig.hexdigest()

        url = "{0}?sig={1}".format(GROOVESHARK_SSL_ENDPOINT,
                                   sig)

        response = requests.post(url, data=json.dumps(payload))
        response = json.loads(response.content)

        result = response.get("result", None)
        if result is None:
            raise RequestErrorException(response)
        else:
            return response

    def _establish_session(self, user_login, user_pass):
        params = {
            'login': user_login,
            'password': user_pass
        }
        response = self._request(method="authenticate", params=params,
                                 sessionID=True)

        result = response.get("result")
        if not result.get("success", False):
            raise InvalidCredentialsException("Invalid Login" +
                                              " or Password.")
        else:
            return result

    def _get_new_session(self):
        response = self._request(method="startSession")
        result = response.get("result", None)
        return result.get("sessionID")

    def get_user_playlists(self, limit=None):
        params = {}
        try:
            if limit is not None:
                limit = int(limit)
                params.update({'limit': limit})
        except ValueError:
            raise InvalidArgumentValueException
        response = self._request(method="getUserPlaylists",
                                 params=params, sessionID=True)
        return response

    def get_playlist(self, playlist_id, limit=None):
        try:
            playlist_id = int(playlist_id)
            params = {'playlistID': playlist_id}

            if limit is not None:
                limit = int(limit)
                params.update({'limit': limit})
        except ValueError:
            raise InvalidArgumentValueException

        response = self._request(method="getPlaylist", params=params)
        return response

    def get_does_song_exist(self, song_id):
        params = {'songID': song_id}
        response = self._request(method='getDoesSongExist', params=params)
        return response.get('result', None)

    def get_songs_info(self, songs_id):
        params = {'songIDs': songs_id}
        response = self._request(method='getSongsInfo', params=params)
        return response.get('result', None)

    def get_stream_key_stream_server(self, song_id, country,
                                     low_bitrate=False):
        params = {'songID': song_id,
                  'country': country,
                  'lowBitrate': low_bitrate}

        response = self._request(method='getStreamKeyStreamServer',
                                 params=params,
                                 sessionID=True)
        return response.get('result', None)

    def get_country(self, ip=None):
        params = {}
        if ip is not None:
            params.update({'ip': ip})
        response = self._request(method='getCountry', params=params)
        return response.get('result', None)

    def get_playlist_search_results(self, query, limit=None):
        params = {'query': query}
        try:
            if limit is not None:
                limit = int(limit)
                params.update({'limit': limit})
        except ValueError:
            raise InvalidArgumentValueException
        response = self._request(method='getPlaylistSearchResults',
                                 params=params)
        return response.get('result', None)

    def get_album_search_results(self, query, limit=None):
        params = {'query': query}
        try:
            if limit is not None:
                limit = int(limit)
                params.update({'limit': limit})
        except ValueError:
            raise InvalidArgumentValueException
        response = self._request(method='getAlbumSearchResults',
                                 params=params)
        return response.get('result', None)

    def get_song_search_results(self, query, country, limit=None, offset=None):
        params = {'query': query, 'country': country}
        try:
            if limit is not None:
                limit = int(limit)
                params.update({'limit': limit})
            if offset is not None:
                offset = int(offset)
                params.update({'offset': offset})
        except ValueError:
            raise InvalidArgumentValueException
        response = self._request(method='getSongSearchResults',
                                 params=params)
        return response.get('result', None)

    def get_artist_search_results(self, query, limit=None):
        params = {'query': query}
        try:
            if limit is not None:
                limit = int(limit)
                params.update({'limit': limit})
        except ValueError:
            raise InvalidArgumentValueException
        response = self._request(method='getArtistSearchResults',
                                 params=params)
        return response.get('result', None)

    def get_autocomplete_search_results(self, query, query_type, limit=None):
        params = {'query': query, 'type': query_type}
        try:
            if limit is not None:
                limit = int(limit)
                params.update({'limit': limit})
        except ValueError:
            raise InvalidArgumentValueException
        response = self._request(method='getAutocompleteSearchResults',
                                 params=params)
        return response.get('result', None)

    def add_user_library_songs(self, song_ids, album_ids, artist_ids):
        params = {'songIDs': song_ids,
                  'albumIDs': album_ids,
                  'artistIDs': artist_ids}

        response = self._request(method='addUserLibrarySongs', params=params,
                                 sessionID=True)
        return response.get('result', None)

    def get_user_library_songs(self, limit=None, page=None):
        params = {}

        try:
            if limit is not None:
                limit = int(limit)
                params.update({'limit': limit})

            if page is not None:
                page = int(page)
                params.update({'page': page})
        except ValueError:
            raise InvalidArgumentValueException

        response = self._request(method='getUserLibrarySongs', params=params,
                                 sessionID=True)
        return response.get('result', None)

    def add_user_library_songs_ex(self, songs):
        params = {'songs': songs}

        response = self._request(method='addUserLibrarySongsEx', params=params,
                                 sessionID=True)
        return response.get('result', None)

    def remove_user_library_songs(self, song_ids, album_ids, artist_ids):
        params = {'songIDs': song_ids,
                  'albumIDs': album_ids,
                  'artistIDs': artist_ids}

        response = self._request(method='removeUserLibrarySongs',
                                 params=params, sessionID=True)
        return response.get('result', None)

    def get_user_playlists_subscribed(self):
        response = self._request(method='getUserPlaylistsSubscribed',
                                 sessionID=True)
        return response.get('result', None)

    def get_user_favorite_songs(self, limit=None):
        params = {}

        try:
            if limit is not None:
                limit = int(limit)
                params.update({'limit': limit})
        except ValueError:
            raise InvalidArgumentValueException

        response = self._request(method='getUserFavoriteSongs', params=params,
                                 sessionID=True)
        return response.get('result', None)

    def remove_user_favorite_songs(self, song_ids):
        params = {'songIDs': song_ids}

        response = self._request(method='removeUserFavoriteSongs',
                                 params=params, sessionID=True)
        return response.get('result', None)

    def logout(self):
        response = self._request(method='removeUserFavoriteSongs',
                                 sessionID=True)
        return response.get('result', None)

    def get_user_info(self):
        response = self._request(method='getUserInfo',
                                 sessionID=True)
        return response.get('result', None)

    def get_user_subscription_details(self):
        response = self._request(method='getUserSubscriptionDetails',
                                 sessionID=True)
        return response.get('result', None)

    def add_user_favorite_song(self, song_id):
        try:
            params = {'songID': int(song_id)}
        except ValueError:
            raise InvalidArgumentValueException

        response = self._request(method='addUserFavoriteSong',
                                 params=params, sessionID=True)
        return response.get('result', None)

    def subscribe_playlist(self, playlist_id):
        try:
            params = {'playlistID': int(playlist_id)}
        except ValueError:
            raise InvalidArgumentValueException

        response = self._request(method='subscribePlaylist',
                                 params=params, sessionID=True)
        return response.get('result', None)

    def unsubscribe_playlist(self, playlist_id):
        try:
            params = {'playlistID': int(playlist_id)}
        except ValueError:
            raise InvalidArgumentValueException

        response = self._request(method='unsubscribePlaylist',
                                 params=params, sessionID=True)
        return response.get('result', None)

    def get_playlist_info(self, playlist_id):
        try:
            params = {'playlistID': int(playlist_id)}
        except ValueError:
            raise InvalidArgumentValueException

        response = self._request(method='getPlaylistInfo',
                                 params=params)
        return response.get('result', None)

    def get_popular_songs_today(self, limit=None):
        params = {}

        try:
            if limit is not None:
                limit = int(limit)
                params.update({'limit': limit})
        except ValueError:
            raise InvalidArgumentValueException

        response = self._request(method='getPopularSongsToday',
                                 params=params)
        return response.get('result', None)

    def get_popular_songs_month(self, limit=None):
        params = {}

        try:
            if limit is not None:
                limit = int(limit)
                params.update({'limit': limit})
        except ValueError:
            raise InvalidArgumentValueException

        response = self._request(method='getPopularSongsMonth',
                                 params=params)
        return response.get('result', None)

    def ping_service(self):
        response = self._request(method='pingService')
        return response.get('result', None)

    def get_service_description(self):
        response = self._request(method='getServiceDescription')
        return response.get('result', None)

    def undelete_playlist(self, playlist_id):
        try:
            params = {'playlistID': int(playlist_id)}
        except ValueError:
            raise InvalidArgumentValueException

        response = self._request(method='undeletePlaylist',
                                 params=params, sessionID=True)
        return response.get('result', None)

    def delete_playlist(self, playlist_id):
        try:
            params = {'playlistID': int(playlist_id)}
        except ValueError:
            raise InvalidArgumentValueException

        response = self._request(method='deletePlaylist',
                                 params=params, sessionID=True)
        return response.get('result', None)

    def get_playlist_songs(self, playlist_id, limit=None):
        try:
            params = {'playlistID': int(playlist_id)}
            if limit is not None:
                limit = int(limit)
                params.update({'limit': limit})
        except ValueError:
            raise InvalidArgumentValueException

        response = self._request(method='getPlaylistSongs',
                                 params=params)
        return response.get('result', None)

    def set_playlist_songs(self, playlist_id, song_ids):
        params = {'playlistID': int(playlist_id),
                  'songIDs': song_ids}

        response = self._request(method='setPlaylistSongs',
                                 params=params, sessionID=True)
        return response.get('result', None)

    def create_playlist(self, name, song_ids):
        params = {'name': name,
                  'songIDs': song_ids}

        response = self._request(method='createPlaylist',
                                 params=params, sessionID=True)
        return response.get('result', None)

    def rename_playlist(self, playlist_id, name):
        params = {'playlistID': int(playlist_id),
                  'name': name}

        response = self._request(method='renamePlaylist',
                                 params=params, sessionID=True)
        return response.get('result', None)

    def get_user_id_from_username(self, username):
        params = {'username': username}
        response = self._request(method='getUserIDFromUsername',
                                 params=params)
        return response.get('result', None)

    def get_albums_info(self, album_ids):
        params = {'albumIDs': album_ids}
        response = self._request(method='getAlbumsInfo',
                                 params=params)
        return response.get('result', None)

    def get_album_songs(self, album_id, limit=None):
        params = {'albumID': album_id}
        try:
            if limit is not None:
                limit = int(limit)
                params.update({'limit': limit})
        except ValueError:
            raise InvalidArgumentValueException

        response = self._request(method='getAlbumSongs',
                                 params=params)
        return response.get('result', None)

    def get_artists_info(self, album_ids):
        params = {'albumIDs': album_ids}
        response = self._request(method='getArtistsInfo',
                                 params=params)
        return response.get('result', None)

    def get_does_album_exist(self, album_id):
        params = {'albumID': album_id}
        response = self._request(method='getDoesAlbumExist', params=params)
        return response.get('result', None)

    def get_does_artist_exist(self, artist_id):
        params = {'artistID': artist_id}
        response = self._request(method='getDoesArtistExist', params=params)
        return response.get('result', None)

    def get_artist_verified_albums(self, artist_id):
        params = {'artistID': artist_id}
        response = self._request(method='getArtistVerifiedAlbums',
                                 params=params)
        return response.get('result', None)

    def get_artist_albums(self, artist_id):
        params = {'artistID': artist_id}
        response = self._request(method='getArtistAlbums',
                                 params=params)
        return response.get('result', None)

    def get_artist_popular_songs(self, artist_id):
        params = {'artistID': artist_id}
        response = self._request(method='getArtistPopularSongs',
                                 params=params)
        return response.get('result', None)
