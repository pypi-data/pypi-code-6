#!/usr/bin/env python


class Hand(object):
    def __init__(self, lst):
        self.cards = lst
        self.values, self.suits = self.set_cards(lst)

    # extract values and suits information from cards
    def set_cards(self, l):
        values = []
        suits = []
        for x in l:
            #print x
            suits.append(x[-1])
            if x[0] == 'J':
                values.append(11)
            elif x[0] == 'Q':
                values.append(12)
            elif x[0] == 'K':
                values.append(13)
            elif x[0] == 'A':
                values.append(14)
            else:
                values.append(int(x[:len(x)-1]))
        return sorted(values), suits

    def has_royal_flush(self):
        hand = self.values
        return self.has_flush() and self.has_straight() and hand[0] == 10

    def has_straight_flush(self):
        hand = self.values
        return self.has_flush() and self.has_straight()

    def has_straight(self):
        for i in range(0, len(self.values)-2):
            if self.values[i]+1 != self.values[i+1]:
                return False
        return True

    def has_pair(self):
        pair = False
        hand = self.values
        a_list = lambda i: [element for element in set(i) if i.count(element) == 2]
        pair_vals = a_list(hand)

        if pair_vals:
            pair = True
        return pair

    def has_three_kind(self):
        trips = False
        hand = self.values
        a_list = lambda i: [element for element in set(i) if i.count(element) == 3]
        trips_vals = a_list(hand)

        if trips_vals:
            trips = True
        return trips

    def has_four_kind(self):
        quad = False
        hand = self.values
        a_list = lambda i: [element for element in set(i) if i.count(element) == 4]
        quad_vals = a_list(hand)

        if quad_vals:
            quad = True
        return quad

    def has_two_pair(self):
        two_pair = False
        hand = self.values
        a_dict = {}
        count = 0

        for element in hand:
            a_dict[element] = hand.count(element)

        for key in a_dict:
            if a_dict[key] == 2:
                count += 1

        if count == 2:
            two_pair = True

        return two_pair

    def has_full_house(self):
        hand=self.values
        return ((hand[0] == hand[1] and hand[1] == hand[2] and hand[2] != hand[3] and hand[3] == hand[4]) or
               (hand[0] == hand[1] and hand[1] != hand[2] and hand[2] == hand[3] and hand[3] == hand[4]))

    def has_flush(self):
        suits = self.suits
        return suits[0] == suits[1] and suits[1] == suits[2] and suits[2] == suits[3] and suits[3] == suits[3]

    def get_rank(self):
        final = 'High Card'
        if self.has_pair():
            final = 'Pair!'
        if self.has_two_pair():
            final = 'Two pairs!'
        if self.has_three_kind():
            final = 'Three of a kind!'
        if self.has_straight():
            final = 'Straight'
        if self.has_flush():
            final = 'Flush'
        if self.has_full_house():
            final = 'Full house!'
        if self.has_four_kind():
            final = 'Four of a kind!'
        if self.has_straight_flush():
            final = "Straight Flush!"
        if self.has_royal_flush():
            final = "Royal Flush!"
        return final