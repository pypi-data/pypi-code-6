# -*- coding: utf-8 -*-

from . import Resource
from ..regions import AVAILABLE_REGIONS


class GamesApi(Resource):
    def __init__(self, api):
        super(GamesApi, self).__init__(api)
        self._version = 'v1.3'
        self._available_regions = AVAILABLE_REGIONS

    def get_recent(self, sid):
        """
        Retrieve recent games by summoner ID.

        :param sid: summoner ID
        """
        return self._get(['game/by-summoner', sid, 'recent'])