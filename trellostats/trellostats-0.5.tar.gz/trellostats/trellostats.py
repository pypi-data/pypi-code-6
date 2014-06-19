# -*- coding: utf-8 -*-
import requests
import grequests

import numpy as np
from dateutil.parser import parse

from settings import ACTION_URL, BOARD_URL, LIST_URL


class TrelloStats(object):
    """
        Main class that does the API thingummy.
        We want to do it direct as we'll be making lots of calls
        around card history, so need to be able to make them in parallel.
    """

    def __init__(self, trellis_context):
        self.app_key = trellis_context.get('app_key')
        self.app_token = trellis_context.get('app_token')
        self.board_id = trellis_context.get('board_id')

    def _do_get(self, url):
        try:
            return requests.get(url).json()
        except ValueError:
            print "Invalid options - check your board id."

    def get_lists(self):
        url = BOARD_URL.format(self.board_id, self.app_key,
                                        self.app_token)
        return self._do_get(url)

    def get_list_id_from_name(self, name):
        try:
            return [li.get('id') for li in self.get_lists()
                    if li.get('name') == name][0]
        except IndexError:
            pass

    def get_list_data(self, list_id):
        url = LIST_URL.format(list_id, self.app_key, self.app_token)
        return self._do_get(url)

    def _get_history_for_cards(self, cards):
        urls = [ACTION_URL.format(card.get('id'), self.app_key,
                                           self.app_token)
                for card in cards]
        rs = (grequests.get(u) for u in urls)
        return grequests.map(rs)

    def _get_cycle_time(self, card_history, units='days'):
        dates = (x.get('date') for x in card_history.json())
        date_objects = sorted([parse(date) for date in dates])
        return getattr((date_objects[-1] - date_objects[0]), units)

    def cycle_time(self, cards):
        try:
            card_histories = self._get_history_for_cards(cards.get('cards'))
            cycle_time = np.mean([self._get_cycle_time(card_history)
                                  for card_history in card_histories])
            return cycle_time
        except AttributeError:
            print "Can't get history of None. Have you put in the correct title of the Done column?"
            exit()

    def __repr__(self):
        return "<TrelloStats: {}>".format(self.app_token)
