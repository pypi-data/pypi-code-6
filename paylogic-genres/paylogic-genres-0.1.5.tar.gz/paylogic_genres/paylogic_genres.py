import json
import os
from bidict import bidict


def _set_genre_cache():
    dirname = os.path.join(os.path.dirname(__file__), 'paylogic_genres.json')
    genre_file = open(dirname)
    genres = json.load(genre_file)
    genre_file.close()
    return genres, bidict([(genre_code, genres[genre_code]['ecc']) for genre_code in genres])


def convert_ecc_to_code(ecc):
    return _GENRE_CACHE[:ecc]


def convert_code_to_ecc(code):
    return _GENRE_CACHE[code]


GENRE_DEFINITIONS, _GENRE_CACHE = _set_genre_cache()
