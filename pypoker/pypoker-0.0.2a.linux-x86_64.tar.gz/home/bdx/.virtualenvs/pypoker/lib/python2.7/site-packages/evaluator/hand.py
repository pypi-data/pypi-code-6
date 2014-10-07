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
        hand = self.values
        return ((hand[0] == hand[1] and hand[1] != hand[2] and hand[2] != hand[3] and hand[3] != hand[4]) or
               (hand[0] != hand[1] and hand[1] == hand[2] and hand[2] != hand[3] and hand[3] != hand[4]) or
               (hand[0] != hand[1] and hand[1] != hand[2] and hand[2] == hand[3] and hand[3] != hand[4]) or
               (hand[0] != hand[1] and hand[1] != hand[2] and hand[2] != hand[3] and hand[3] == hand[4]))

    def has_three_kind(self):
        hand = self.values
        return ((hand[0] == hand[1] and hand[1] == hand[2] and hand[2] != hand[3] and hand[3] != hand[4]) or
               (hand[0] != hand[1] and hand[1] == hand[2] and hand[2] == hand[3] and hand[3] != hand[4]) or
               (hand[0] != hand[1] and hand[1] != hand[2] and hand[2] == hand[3] and hand[3] == hand[4]))

    def has_four_kind(self):
        hand = self.values
        return ((hand[0] == hand[1] and hand[1] == hand[2] and hand[2] == hand[3] and hand[3] != hand[4]) or
               (hand[0] != hand[1] and hand[1] == hand[2] and hand[2] == hand[3] and hand[3] == hand[4]))

    def has_two_pair(self):
        hand=self.values
        return ((hand[0] == hand[1] and hand[1] != hand[2] and hand[2] == hand[3] and hand[3] != hand[4]) or
               (hand[0] == hand[1] and hand[1] != hand[2] and hand[2] != hand[3] and hand[3] == hand[4]) or
               (hand[0] != hand[1] and hand[1] == hand[2] and hand[2] != hand[3] and hand[3] == hand[4]))

    def has_full_house(self):
        hand=self.values
        return ((hand[0] == hand[1] and hand[1] == hand[2] and hand[2] != hand[3] and hand[3] == hand[4]) or
               (hand[0] == hand[1] and hand[1] != hand[2] and hand[2] == hand[3] and hand[3] == hand[4]))

    def has_flush(self):
        s=self.suits
        return s[0] == s[1] and s[1] == s[2] and s[2] == s[3] and s[3] == s[4]

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
