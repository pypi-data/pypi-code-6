# -*- coding: utf-8 -*-

from . import Resource
from ..regions import AVAILABLE_REGIONS


class StaticDataApi(Resource):
    def __init__(self, api):
        super(StaticDataApi, self).__init__(api)
        # * Note: The static data is a global service,
        # and thus uses the global.api.pvp.net endpoint
        # regardless of the region selected. For example,
        # this URL returns KR-specific data:
        #
        # https://global.api.pvp.net/api/lol/static-data/kr/v1.2/champion/41?champData=image&api_key=<key>
        self._netloc = u'global.api.pvp.net'
        self._version = 'v1.2'
        self._available_regions = AVAILABLE_REGIONS

    @property
    def _base_uri(self):  # a little janky, had to override because of Riot's inconsistent uri structure
        return u'/'.join(['/api/lol', 'static-data', self._api._region, self._version])

    def get_champions(self):
        """
        Retrieves champion list.
        """
        return self._get(['champion'])

    def get_champion_by_id(self, cid):
        """
        Retrieves a champion by its ID.

        :param cid: champion ID
        """
        return self._get(['champion', cid])

    def get_items(self):
        """
        Retrieves item list.
        """
        return self._get(['item'])

    def get_item_by_id(self, iid):
        """
        Retrieves an item by its ID.

        :param iid: item ID
        """
        return self._get(['item', iid])

    def get_masteries(self):
        """
        Retrieves mastery list.
        """
        return self._get(['mastery'])

    def get_mastery_by_id(self, mid):
        """
        Retrieves mastery item by its ID.

        :param mid: mastery ID
        """
        return self._get(['mastery', mid])

    def get_realms(self):
        """
        Retrieve realm data.
        """
        return self._get(['realm'])

    def get_runes(self):
        """
        Retrieves rune list.
        """
        return self._get(['rune'])

    def get_rune_by_id(self, rid):
        """
        Retrieves rune by its ID.

        :param rid: rune ID
        """
        return self._get(['rune', rid])

    def get_summoner_spells(self):
        """
        Retrieves summoner spell list.
        """
        return self._get(['summoner-spell'])

    def get_summoner_spell_by_id(self, sid):
        """
        Retrieves summoner spell by its ID.

        :param sid: spell ID
        """
        return self._get(['summoner-spell', sid])

    def get_versions(self):
        """
        Retrieves game version data.
        """
        return self._get(['versions'])