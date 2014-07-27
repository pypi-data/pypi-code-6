# -*- coding: utf-8 -*-

"""
lolapi.api
==========

This module implements the top-level API.

:author: Steven Motes
:license: MIT, see LICENSE for more details.

"""


class LolApi(object):
    """
    Top-level API, consisting of a collection of resources.

    @region: valid region in ['br', 'eune', 'euw', 'lan', 'las', 'na', 'oce', 'ru']
    @key: API key  
    """

    def __init__(self, region, key):
        self.set_region(region)
        self._key = key

        # setup resources
        from resources.champions import ChampionsApi

        self.champions = ChampionsApi(self)

        from resources.games import GamesApi

        self.games = GamesApi(self)

        from resources.summoners import SummonersApi

        self.summoners = SummonersApi(self)

        from resources.teams import TeamsApi

        self.teams = TeamsApi(self)

        from resources.leagues import LeaguesApi

        self.leagues = LeaguesApi(self)

        from resources.stats import StatsApi

        self.stats = StatsApi(self)

        from resources.data import StaticDataApi

        self.data = StaticDataApi(self)

    def set_region(self, region):
        """ Validates region. """
        from exceptions import UnsupportedRegion

        if region not in ['br', 'eune', 'euw', 'lan', 'las', 'na', 'oce', 'ru']:
            raise UnsupportedRegion()
        self._region = region

    def get_key(self):
        return self._key

    def get_region(self):
        return self._region