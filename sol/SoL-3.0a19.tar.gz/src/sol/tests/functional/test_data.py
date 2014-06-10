# -*- coding: utf-8 -*-
# :Progetto:  SoL -- Tests for the data controller
# :Creato:    mer 15 ott 2008 08:27:03 CEST
# :Autore:    Lele Gaifax <lele@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later
#

from . import AuthenticatedTestCase


class TestDataViews(AuthenticatedTestCase):
    def test_clubs(self):
        from .. import ClubData

        response = self.app.get('/data/clubs')
        result = response.json
        self.assertEqual(result['success'], True)
        self.assertEqual(result['message'], "Ok")
        self.assertEqual(result['count'], len(ClubData.rows))

    def test_club(self):
        from .. import ClubData

        response = self.app.get('/data/clubs?filter_description='
                                + ClubData.scr.description)
        result = response.json
        self.assertEqual(result['success'], True)
        self.assertEqual(result['message'], "Ok")
        self.assertEqual(result['count'], 1)
        club = result['root'][0]
        self.assertEqual(club['description'],
                         ClubData.scr.description)
        self.assertEqual(club['Championships'], 5)

    def test_federations(self):
        response = self.app.get('/data/federations')
        result = response.json
        self.assertEqual(result['success'], True)
        self.assertEqual(result['message'], "Ok")
        self.assertEqual(result['count'], 1)

    def test_players(self):
        from .. import PlayerData

        response = self.app.get('/data/players')
        result = response.json
        self.assertEqual(result['success'], True)
        self.assertEqual(result['message'], "Ok")
        self.assertEqual(result['count'], len(PlayerData.rows))
        for p in result['root']:
            if p['firstname'] == 'Fata':
                self.assertEqual(p['Language'], 'Zulu')
                break
        else:
            assert False, "No Fata??"

    def test_player(self):
        from .. import PlayerData, TourneyData

        response = self.app.get('/data/players?filter_nickname='
                                + PlayerData.lele.nickname)
        result = response.json
        self.assertEqual(result['success'], True)
        self.assertEqual(result['message'], "Ok")
        self.assertEqual(result['count'], 1)
        player = result['root'][0]
        self.assertEqual(player['firstname'],
                         PlayerData.lele.firstname)
        self.assertEqual(player['lastname'],
                         PlayerData.lele.lastname)
        self.assertEqual(player['LastPlayed'],
                         TourneyData.dazedodd.date.isoformat())

    def test_championships(self):
        from .. import ChampionshipData

        response = self.app.get('/data/championships')
        result = response.json
        self.assertEqual(result['success'], True)
        self.assertEqual(result['message'], "Ok")
        self.assertEqual(result['count'], len(ChampionshipData.rows))

    def test_championship(self):
        from .. import ClubData, ChampionshipData

        response = self.app.get('/data/championships?filter_description='
                                + ChampionshipData.scr2010.description)
        result = response.json
        self.assertEqual(result['success'], True)
        self.assertEqual(result['message'], "Ok")
        self.assertEqual(result['count'], 1)
        championship = result['root'][0]
        self.assertEqual(championship['description'], ChampionshipData.scr2010.description)
        self.assertEqual(championship['Club'], ClubData.scr.description)

    def test_tourneys(self):
        from .. import TourneyData

        response = self.app.get('/data/tourneys')
        result = response.json
        self.assertEqual(result['success'], True)
        self.assertEqual(result['message'], "Ok")
        self.assertEqual(result['count'], len(TourneyData.rows))

    def test_player_tourneys(self):
        from .. import PlayerData

        response = self.app.get('/data/players?filter_lastname='
                                + PlayerData.fata.lastname)
        result = response.json

        response = self.app.get('/data/tourneys?idplayer=%d' %
                                result['root'][0]['idplayer'])
        result = response.json
        self.assertEqual(result['success'], True)
        self.assertEqual(result['message'], "Ok")
        self.assertEqual(result['count'], 6)

    def test_tourney(self):
        from .. import TourneyData

        response = self.app.get('/data/tourneys?filter_description='
                                + TourneyData.first.description)
        result = response.json
        self.assertEqual(result['success'], True)
        self.assertEqual(result['message'], "Ok")
        self.assertEqual(result['count'], 1)
        tourney = result['root'][0]
        self.assertEqual(tourney['description'],
                         TourneyData.first.description)
        self.assertEqual(tourney['date'],
                         TourneyData.first.date.isoformat())
        self.assertEqual(tourney['Championship'],
                         TourneyData.first.championship.description)

    def test_countries(self):
        response = self.app.get('/data/countries')
        result = response.json
        self.assertEqual(result['success'], True)
        self.assertEqual(result['message'], "Ok")
        self.assertEqual(set(result['root'][0].keys()), set(['code', 'name']))

    def test_languages(self):
        response = self.app.get('/data/languages')
        result = response.json
        self.assertEqual(result['success'], True)
        self.assertEqual(result['message'], "Ok")
        self.assertEqual(set(result['root'][0].keys()), set(['code', 'name']))

    def test_ratings(self):
        from .. import PlayerData, RatingData

        response = self.app.get('/data/ratings')
        result = response.json
        self.assertEqual(result['success'], True)
        self.assertEqual(result['message'], "Ok")
        self.assertEqual(result['count'], len(RatingData.rows))
        self.assertEqual(result['root'][0]['description'],
                         RatingData.european.description)
        self.assertEqual(result['root'][0]['Players'], 5)
        self.assertEqual(result['root'][0]['Tourneys'], 1)

        idrating = result['root'][0]['idrating']

        response = self.app.get('/data/ratedPlayers?filter_idrating=%d' % idrating)
        result = response.json
        self.assertEqual(result['success'], True)
        self.assertEqual(result['message'], "Ok")
        self.assertEqual(result['count'], 5)
        self.assertEqual(result['root'][0]['lastname'], PlayerData.varechina.lastname)
