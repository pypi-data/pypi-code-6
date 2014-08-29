# -*- coding: utf-8 -*-

import regions

"""
lolapi
==========

This module implements the top-level API.

:author: smotes
:license: MIT, see LICENSE for more details.
:version: 0.9.6

"""

__name__ = 'lolapi'
__author__ = 'smotes'
__version__ = '0.9.8'
__license__ = 'MIT'


class LolApi(object):
    """
    Top-level API, consisting of a collection of resources.

    :param region: valid region in ['br', 'eune', 'euw', 'lan', 'las', 'na', 'oce', 'ru']
    :param key: League of Legends API key
    """

    def __init__(self, region, key):
        self._set_region(region)
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

    def _set_region(self, region):
        """
        Validates region.

        :param region: API region as `str`.
        """
        from regions import AVAILABLE_REGIONS
        from exceptions import UnsupportedRegion

        if region not in AVAILABLE_REGIONS:
            raise UnsupportedRegion()
        self._region = region
