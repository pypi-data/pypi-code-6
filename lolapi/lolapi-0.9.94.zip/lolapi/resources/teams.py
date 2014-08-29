# -*- coding: utf-8 -*-

from . import Resource
from ..regions import AVAILABLE_REGIONS


class TeamsApi(Resource):
    def __init__(self, api):
        super(TeamsApi, self).__init__(api)
        self._version = 'v2.3'
        self._available_regions = AVAILABLE_REGIONS

    def get_by_summoners(self, sids):
        """
        Get teams mapped by summoner ID for a given list of summoner IDs.
        
        :param sids: list of summoner IDs
        """
        return self._get(['team', 'by-summoner', u','.join(sids)])

    def get_by_ids(self, tids):
        """
        Get teams mapped by team IDs for a given list of team IDs.

        :param tids: list of team IDs
        """
        return self._get(['team', u','.join(tids)])