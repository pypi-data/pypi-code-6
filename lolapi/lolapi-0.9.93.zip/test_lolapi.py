#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys

try:
    import _keys
except ImportError:
    sys.exit("Exiting unit tests...\nREASON: no API key provided")

import unittest
import lolapi
import lolapi.exceptions as api_exceptions


class TestLolApi(unittest.TestCase):
    def get_current_version(self):
        """ Helper method to explicitly get most current game version from the API. """
        import requests
        url = 'https://na.api.pvp.net/api/lol/static-data/na/v1.2/versions?api_key=%s' % _keys.API_KEY
        r = requests.get(url)
        return unicode(r.json()[0])  # most current version is always first in list

    def setUp(self):
        self.GAME_VERSION = self.get_current_version()
        from lolapi.regions import AVAILABLE_REGIONS

        self.apis = {}
        for region in AVAILABLE_REGIONS:
            self.apis[region] = lolapi.LolApi(region=region, key=_keys.API_KEY)

        # variables used throughout unittests
        self.CHAMPION_COUNT = 120
        self.ITEM_COUNT = 252
        self.MASTERY_COUNT = 57
        self.RUNE_COUNT = 296
        self.SUMMONER_SPELL_COUNT = 13
        self.GAME_VERSION_COUNT = 78
        self.SUMMONER_NAMES = [u'man', u'girl']

    def wait(self):
        """ Helper method used to pause for one second to avoid hitting the API rate limit during unit tests. """
        time.sleep(1)  # pause for 1 second

    def _test_champions_api(self, api):
        assert api.champions._version == 'v1.2'
        #
        # Retrieve champion list
        #
        data = api.champions.get_all()
        assert isinstance(data, dict)
        assert isinstance(data['champions'], list)
        assert isinstance(data['champions'][0], dict)
        assert len(data['champions']) > 100
        champion = data['champions'][0]  # id = 266
        self.wait()

        #
        # Retrieve champion by ID
        #
        data = api.champions.get_by_id(champion['id'])
        assert isinstance(data, dict)
        assert isinstance(data['botMmEnabled'], bool)
        assert isinstance(data['id'], int)
        assert isinstance(data['rankedPlayEnabled'], int)
        assert isinstance(data['botEnabled'], bool)
        assert isinstance(data['active'], bool)
        assert isinstance(data['freeToPlay'], bool)
        self.wait()

        #
        # Retrieve champion by invalid ID
        #
        with self.assertRaises(api_exceptions.NotFound) as cmd:
            api.champions.get_by_id(5000)

    def test_champions_apis(self):
        for key in self.apis:
            self._test_champions_api(self.apis[key])

    def _test_data_api(self, api):
        assert api.data._version == 'v1.2'

        #
        # Retrieve champion list
        #
        data = api.data.get_champions()
        assert isinstance(data, dict)
        assert data['type'] == 'champion'
        assert data['version'] == self.GAME_VERSION
        assert isinstance(data['data'], dict)
        assert len(data['data']) == self.CHAMPION_COUNT
        champion = data['data'].itervalues().next()
        assert isinstance(champion['id'], int)
        assert isinstance(champion['key'], unicode)
        assert isinstance(champion['name'], unicode)
        assert isinstance(champion['title'], unicode)

        #
        # Retrieve champion by ID
        #
        data = api.data.get_champion_by_id(champion['id'])
        assert isinstance(data, dict)
        assert isinstance(data['id'], int)
        assert data['id'] == champion['id']
        assert isinstance(data['key'], unicode)
        assert data['key'] == champion['key']
        assert isinstance(data['name'], unicode)
        assert data['name'] == champion['name']
        assert isinstance(data['title'], unicode)
        assert data['title'] == champion['title']

        #
        # Retrieve item list
        #
        data = api.data.get_items()
        assert isinstance(data, dict)
        assert data['type'] == 'item'
        assert data['version'] == '4.13.1'
        assert isinstance(data['basic'], dict)
        assert isinstance(data['basic']['id'], int)
        assert isinstance(data['data'], dict)
        assert len(data['data']) == self.ITEM_COUNT
        item = data['data'].itervalues().next()
        assert isinstance(item['id'], int)
        assert isinstance(item['name'], unicode)
        assert isinstance(item['description'], unicode)
        assert isinstance(item['plaintext'], unicode)

        #
        # Retrieve item by ID
        #
        data = api.data.get_item_by_id(item['id'])
        assert isinstance(data, dict)
        assert isinstance(data['id'], int)
        assert data['id'] == item['id']
        assert isinstance(data['plaintext'], unicode)
        assert data['plaintext'] == item['plaintext']
        assert isinstance(data['name'], unicode)
        assert data['name'] == item['name']
        assert isinstance(data['description'], unicode)
        assert data['description'] == item['description']

        #
        # Retrieve mastery list
        #
        data = api.data.get_masteries()
        assert isinstance(data, dict)
        assert data['type'] == 'mastery'
        assert data['version'] == self.GAME_VERSION
        assert isinstance(data['data'], dict)
        assert len(data['data']) == self.MASTERY_COUNT
        mastery = data['data'].itervalues().next()
        assert isinstance(mastery['id'], int)
        assert isinstance(mastery['name'], unicode)
        assert isinstance(mastery['description'], list)
        assert len(mastery['description']) >= 1
        assert isinstance(mastery['description'][0], unicode)

        #
        # Retrieve mastery by ID
        #
        data = api.data.get_mastery_by_id(mastery['id'])
        assert isinstance(data, dict)
        assert isinstance(data['id'], int)
        assert data['id'] == mastery['id']
        assert isinstance(data['name'], unicode)
        assert data['name'] == mastery['name']
        assert isinstance(data['description'], list)
        assert data['description'][0] == mastery['description'][0]

        #
        # Retrieve realm list
        #
        data = api.data.get_realms()
        assert isinstance(data, dict)
        assert isinstance(data['v'], unicode)
        assert isinstance(data['dd'], unicode)
        assert isinstance(data['cdn'], unicode)
        assert isinstance(data['lg'], unicode)
        assert isinstance(data['n'], dict)
        assert isinstance(data['profileiconmax'], int)
        assert isinstance(data['l'], unicode)
        assert isinstance(data['css'], unicode)

        #
        # Retrieve rune list
        #
        data = api.data.get_runes()
        assert isinstance(data, dict)
        assert data['type'] == 'rune'
        assert data['version'] == self.GAME_VERSION
        assert isinstance(data['data'], dict)
        assert len(data['data']) == self.RUNE_COUNT
        rune = data['data'].itervalues().next()
        assert isinstance(rune['id'], int)
        assert isinstance(rune['name'], unicode)
        assert isinstance(rune['description'], unicode)
        assert isinstance(rune['rune'], dict)
        assert isinstance(rune['rune']['isRune'], bool)
        assert isinstance(rune['rune']['tier'], unicode)
        assert isinstance(rune['rune']['type'], unicode)

        #
        # Retrieve rune by ID
        #
        data = api.data.get_rune_by_id(rune['id'])
        assert isinstance(data, dict)
        assert isinstance(data['id'], int)
        assert data['id'] == rune['id']
        assert isinstance(data['description'], unicode)
        assert data['description'] == rune['description']
        assert isinstance(data['name'], unicode)
        assert data['name'] == rune['name']
        assert isinstance(data['rune'], dict)
        assert data['rune']['isRune'] == rune['rune']['isRune']
        assert data['rune']['tier'] == rune['rune']['tier']
        assert data['rune']['type'] == rune['rune']['type']

        #
        # Retrieve summoner spell list
        #
        data = api.data.get_summoner_spells()
        assert isinstance(data, dict)
        assert data['type'] == 'summoner'
        assert data['version'] == self.GAME_VERSION
        assert isinstance(data['data'], dict)
        assert len(data['data']) == self.SUMMONER_SPELL_COUNT
        spell = data['data'].itervalues().next()
        assert isinstance(spell['name'], unicode)
        assert isinstance(spell['description'], unicode)
        assert isinstance(spell['summonerLevel'], int)
        assert isinstance(spell['id'], int)
        assert isinstance(spell['key'], unicode)

        #
        # Retrieve summoner spell by ID
        #
        data = api.data.get_summoner_spell_by_id(spell['id'])
        assert isinstance(data, dict)
        assert isinstance(data['id'], int)
        assert data['id'] == spell['id']
        assert isinstance(data['description'], unicode)
        assert data['description'] == spell['description']
        assert isinstance(data['name'], unicode)
        assert data['name'] == spell['name']
        assert isinstance(data['key'], unicode)
        assert data['key'] == spell['key']
        assert isinstance(data['summonerLevel'], int)
        assert data['summonerLevel'] == spell['summonerLevel']

        #
        # Retrieve game version data
        #
        data = api.data.get_versions()
        assert isinstance(data, list)
        assert len(data) == self.GAME_VERSION_COUNT

    def test_data_apis(self):
        for key in self.apis:
            self._test_data_api(self.apis[key])

    def _test_summoners_api(self, api):
        assert api.summoners._version == 'v1.4'

        #
        # Get summoners by list of summoner names
        #
        data = api.summoners.get_by_names(self.SUMMONER_NAMES)
        assert isinstance(data, dict)
        assert len(data) == len(self.SUMMONER_NAMES)
        for name in self.SUMMONER_NAMES:
            self.assertIsNotNone(data.get(name))
        first_summoner = data[self.SUMMONER_NAMES[0]]
        second_summoner = data[self.SUMMONER_NAMES[1]]
        self.wait()

        #
        # Get summoners by list of summoner IDs
        #
        self.SUMMONER_IDS = [
            unicode(first_summoner['id']),
            unicode(second_summoner['id'])
        ]
        data = api.summoners.get_by_ids(self.SUMMONER_IDS)
        assert isinstance(data, dict)
        assert len(data) == len(self.SUMMONER_NAMES)
        first = data.get(unicode(first_summoner['id']))
        second = data.get(unicode(second_summoner['id']))
        self.assertIsNotNone(first)
        self.assertIsNotNone(second)
        self.wait()

        #
        # Get summoner mastery pages by list of summoner IDs
        #
        data = api.summoners.get_masteries(self.SUMMONER_IDS)
        assert isinstance(data, dict)
        assert len(data) == len(self.SUMMONER_NAMES)
        first = data.get(unicode(first_summoner['id']))
        second = data.get(unicode(second_summoner['id']))
        self.assertIsNotNone(first)
        self.assertIsNotNone(second)
        assert unicode(first['summonerId']) in self.SUMMONER_IDS
        assert isinstance(first['pages'], list)
        self.wait()

        #
        # Get summoner names by list of summoner IDs
        #
        data = api.summoners.get_names(self.SUMMONER_IDS)
        assert isinstance(data, dict)
        assert len(data) == len(self.SUMMONER_IDS)
        for key in data:
            assert key in self.SUMMONER_IDS
            assert isinstance(data[key], unicode)
        self.wait()

        #
        # Get summoner runes by list of summoner IDS
        #
        data = api.summoners.get_runes(self.SUMMONER_IDS)
        assert isinstance(data, dict)
        assert len(data) == len(self.SUMMONER_IDS)
        for key in data:
            assert key in self.SUMMONER_IDS
            assert isinstance(data[key], dict)
            assert isinstance(data[key]['summonerId'], int)
            assert isinstance(data[key]['pages'], list)
        self.wait()

    def test_summoners_apis(self):
        for key in self.apis:
            self._test_summoners_api(self.apis[key])

    def _test_games_api(self, api):
        assert api.games._version == 'v1.3'
        data = api.summoners.get_by_names(self.SUMMONER_NAMES)
        first_summoner = data[self.SUMMONER_NAMES[0]]
        second_summoner = data[self.SUMMONER_NAMES[1]]
        self.SUMMONER_IDS = [
            unicode(first_summoner['id']),
            unicode(second_summoner['id'])
        ]

        #
        # Retrieve recent games by summoner ID
        #
        data = api.games.get_recent(self.SUMMONER_IDS[1])
        assert data['summonerId'] == int(self.SUMMONER_IDS[1])
        assert isinstance(data['games'], list)
        assert len(data['games']) <= 10
        game = data['games'][0]
        assert isinstance(game['gameId'], int)
        assert isinstance(game['invalid'], bool)
        assert isinstance(game['fellowPlayers'], list)
        assert len(game['fellowPlayers']) > 0
        assert isinstance(game['stats'], dict)
        assert len(game['stats']) > 15
        self.wait()

    def test_games_apis(self):
        for key in self.apis:
            self._test_games_api(self.apis[key])

    def _test_stats_api(self, api):
        assert api.stats._version == 'v1.3'
        data = api.summoners.get_by_names(self.SUMMONER_NAMES)
        first_summoner = data[self.SUMMONER_NAMES[0]]
        second_summoner = data[self.SUMMONER_NAMES[1]]
        self.SUMMONER_IDS = [
            unicode(first_summoner['id']),
            unicode(second_summoner['id'])
        ]

        #
        # Retrieve ranked stats by summoner ID
        #
        try:
            data = api.stats.get_ranked_stats(self.SUMMONER_IDS[1])
            assert isinstance(data, dict)
            assert isinstance(data['summonerId'], int)
            assert data['summonerId'] == int(self.SUMMONER_IDS[1])
            assert isinstance(data['modifyDate'], long)
            assert isinstance(data['champions'], list)
            assert len(data['champions']) >= 1
        except api_exceptions.NotFound:  # may 404 if player does not play ranked matches
            pass
        self.wait()

        #
        # Retrieve player stats summary by summoner ID
        #
        try:
            data = api.stats.get_summary(self.SUMMONER_IDS[1])
            assert isinstance(data, dict)
            assert isinstance(data['summonerId'], int)
            assert data['summonerId'] == int(self.SUMMONER_IDS[1])
            assert isinstance(data['playerStatSummaries'], list)
            assert len(data['playerStatSummaries']) >= 0
        except api_exceptions.NotFound:
            pass
        self.wait()

    def test_stats_apis(self):
        for key in self.apis:
            self._test_stats_api(self.apis[key])


if __name__ == '__main__':
    unittest.main()