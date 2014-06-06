__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

import os
from urllib import request
from xml.etree import ElementTree

import requests
import bs4

from pymal import decorators
from pymal import Season

__all__ = ['Seasons']


class Seasons(object, metaclass=decorators.Singleton):
    """
    Lazy making of Season from online db.
    
    Attributes:
        seasons: set of Season.
    """
    __all__ = ['seasons', 'reload']

    __HOSTNAME = 'http://github.com'
    __SEASONS_URL = request.urljoin(
        __HOSTNAME, 'erengy/taiga/tree/master/data/db/season')

    def __init__(self):
        self.__seasons = set()
        self._is_loaded = False

    @property
    @decorators.load
    def seasons(self):
        return self.__seasons

    def reload(self):
        sock = requests.get(self.__SEASONS_URL)
        table = bs4.BeautifulSoup(sock.text).find(
            name="table", attrs={'class': 'files'})
        assert table is not None

        contents = table.findAll(name='td', attrs={'class': 'content'})
        assert 0 < len(contents)
        for i in contents:
            xml_url = request.urljoin(self.__HOSTNAME, i.span.a['href'])
            sock = requests.get(xml_url)
            xml_html = sock.text

            xml_body = bs4.BeautifulSoup(xml_html).find(
                name="div", attrs={"class": "code-body"}).text
            xml_element = ElementTree.fromstring(xml_body)

            anime_elements = list(xml_element)
            season_info_elements = anime_elements[0]
            assert 'info' == season_info_elements.tag
            season_name, year = season_info_elements.find('name').text.split()

            animes_ids = set()
            anime_elements = anime_elements[1:]
            for anime_element in anime_elements:
                assert 'anime' == anime_element.tag
                _, series_animedb_id_element, _, _, _ = list(anime_element)
                assert int(series_animedb_id_element.text) not in animes_ids
                animes_ids.add(int(series_animedb_id_element.text))

            season = Season.Season(season_name, year, animes_ids)
            assert season not in self.__seasons
            self.__seasons.add(season)

        self._is_loaded = True

    def __contains__(self, item) -> bool:
        return any(map(lambda x: item in x, self.seasons))

    def __repr__(self):
        return (os.linesep + '\t').join(map(str, ['<Seasons>'] +
                                            list(self.seasons)))

    def __iter__(self):
        class SeasonsIterator(object):

            def __init__(self, values):
                self.values = list(values)
                self.location = 0

            def __iter__(self):
                self.location = 0
                return self

            def __next__(self):
                if self.location >= len(self.values):
                    raise StopIteration
                value = self.values[self.location]
                self.location += 1
                return value
        return SeasonsIterator(self.seasons)

    def __len__(self) -> int:
        return sum(map(lambda x: len(x), self.seasons))
