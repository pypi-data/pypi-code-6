# -*- coding: utf-8 -*-

from . import Resource
from ..regions import AVAILABLE_REGIONS


class LeaguesApi(Resource):
    def __init__(self, api):
        super(LeaguesApi, self).__init__(api)
        self._version = 'v2.4'
        self._available_regions = AVAILABLE_REGIONS

    def get_by_summoners(self, sids):
        """
        Get leagues mapped by summoner ID for a given list of summoner IDs.
        
        :param sids: list of summoner IDs
        """
        return self._get(['league', 'by-summoner', u','.join(sids)])

    def get_entry_by_summoners(self, sids):
        """
        Get league enteries mapped by summoner ID for a given list of summoner IDs.
        
        :param sids: list of summoner IDs
        """
        return self._get(['league', 'by-summoner', u','.join(sids), 'entry'])

    def get_by_team(self, tids):
        """
        Get leagues mapped by by team ID for a given list of team IDs.

        :param tids: list of team IDs
        """
        return self._get(['league', 'by-team', u','.join(tids)])

    def get_entry_by_team(self, tids):
        """
        Get league entries mapped by team ID for a given list of team IDs.

        :param tids: list of team IDs
        """
        return self._get(['league', 'by-team', u','.join(tids), 'entry'])

    def get_challenger(self):
        """
        Get challenger tier leagues.
        """
        return self._get(['league', 'challenger'])