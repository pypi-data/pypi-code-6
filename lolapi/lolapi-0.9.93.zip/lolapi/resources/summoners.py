# -*- coding: utf-8 -*-

from . import Resource
from ..regions import AVAILABLE_REGIONS


class SummonersApi(Resource):
    def __init__(self, api):
        super(SummonersApi, self).__init__(api)
        self._version = 'v1.4'
        self._available_regions = AVAILABLE_REGIONS

    def get_by_names(self, names):
        """
        Get summoners mapped by standardized summoner name for a given list of summoner names.

        :param names: list of summoner names
        """
        return self._get(['summoner', 'by-name', u','.join(names)])

    def get_by_ids(self, sids):
        """
        Get summoners mapped by summoner ID for a given list of summoner IDs.

        :param sids: list of summoner IDs
        """
        return self._get(['summoner', u','.join(sids)])

    def get_masteries(self, sids):
        """
        Get mastery pages mapped by summoner ID for a given list of summoner IDs.

        :param sids: list of summoner IDs
        """
        return self._get(['summoner', u','.join(sids), 'masteries'])

    def get_names(self, sids):
        """
        Get summoner names mapped by a summoner ID for a given list of summoner IDs.

        :param sids: list of summoner IDs
        """
        return self._get(['summoner', u','.join(sids), 'name'])

    def get_runes(self, sids):
        """
        Get summoner rune pages mapped by a summoner ID for a given list of summoner IDs.

        :param sids: list of summoner IDs
        """
        return self._get(['summoner', u','.join(sids), 'runes'])