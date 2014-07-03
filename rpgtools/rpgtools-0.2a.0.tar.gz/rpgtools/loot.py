#!/usr/bin/env python
"""This module generates random Loot from a list (constant from now) based
on weight and item type. Many improvements will be done later.
"""
from collections import Counter, OrderedDict
from pprint import pprint
import bisect
import json
import random


class LootGenerator(object):
    """ Generate loot for RPG Campaigns. """

    def __init__(self, **kwargs):
        #rarities=None, item_types=None, min_level=1,
        #         max_level=10, loot_limit=None
        #TODO: the package's items.json will be used if no items.json exists in
        # the current directory.
        with open('items.json', 'r') as itemfile:
            self.items = json.load(itemfile, object_pairs_hook=OrderedDict)

        #If no rarity values are provided, default weights will be assumed.
        if not kwargs.get('rarities', None):
            rarities = {'common': 10, 'rare': 1.5, 'uncommon': 7.5,
                        'unique': 0.1, 'wondrous': 0.5}

        #Get item types dinamically.
        item_types = list(Counter([value['category'] for value in self.items]))

        self.totals = []
        # noinspection PyUnboundLocalVariable
        self.rarities = rarities
        self.item_types = item_types
        self.min_level = kwargs.get('min_level', 1)
        self.max_level = kwargs.get('max_level', 100)
        self.loot_limit = kwargs.get('loot_limit', 10)
        running_total = 0

        for rarity in rarities.values():
            running_total += rarity
            self.totals.append(running_total)

    def get_items(self, category, rarity, min_level, max_level):
        """ Return a dynamic list within the item[s]. """
        values = [value for value in self.items
                  if value['rarity'] == rarity
                  and value['category'] == category
                  and min_level <= value['level'] <= max_level]
        if values:
            return random.choice(values)
        else:
            return category, rarity

    def next(self):
        """ Invoke a LootItem that returns the item[s]. """
        for loot_item in range(self.loot_limit):
            rnd = random.random() * self.totals[-1]
            score = bisect.bisect(self.totals, rnd)
            item_type, rarity = random.choice(self.item_types), \
                                list(self.rarities.keys())[score]
            item = self.get_items(item_type, rarity, self.min_level,
                                  self.max_level)
            pprint(item)


if __name__ == '__main__':
    LootGenerator().next()
