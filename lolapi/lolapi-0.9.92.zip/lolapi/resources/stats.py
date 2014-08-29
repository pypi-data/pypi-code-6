# -*- coding: utf-8 -*-

from .import Resource
from ..regions import AVAILABLE_REGIONS


class StatsApi(Resource):
    def __init__(self, api):
        super(StatsApi, self).__init__(api)
        self._version = 'v1.3'
        self._available_regions = AVAILABLE_REGIONS

    def get_ranked_stats(self, sid):
        """
        Get ranked stats by summoner ID.

        :param sid: summoner ID
        """
        return self._get(['stats', 'by-summoner', sid, 'ranked'])

    def get_summary(self, sid):
        """
        Get player stats summaries by summoner ID.

        :param sid: summoner ID
        """
        return self._get(['stats', 'by-summoner', sid, 'summary'])