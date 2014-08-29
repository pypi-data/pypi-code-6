# -*- coding: utf-8 -*-

from . import Resource
from ..regions import AVAILABLE_REGIONS


class ChampionsApi(Resource):
    def __init__(self, api):
        super(ChampionsApi, self).__init__(api)
        self._version = 'v1.2'
        self._available_regions = AVAILABLE_REGIONS

    def get_all(self):
        """ 
        Retrieve all champions. 
        """
        return self._get(['champion'])

    def get_by_id(self, cid):
        """ 
        Retrieve champion by ID.

        :param cid: champion ID
        """
        return self._get(['champion', cid])