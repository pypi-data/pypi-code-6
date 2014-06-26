"""
    serialization.py

    defines the serialization mediums used.

    :copyright: (c) Heartland Payment Systems. All rights reserved.
"""

from securesubmit.entities.credit import HpsCreditCard


class HpsError(object):
    type = None
    message = None
    code = None
    param = None

    @classmethod
    def from_dict(cls, data):
        error = cls()
        for key in data:
            setattr(error, key, data[key])
        return error


class HpsToken(object):
    object = None
    token_type = None
    token_value = None
    token_expire = None
    card = None
    error = None

    def __init__(self,
                 card_data=None,
                 cvc=None,
                 exp_month=None,
                 exp_year=None):
        self.object = "token"
        self.token_type = "supt"

        if card_data is not None:
            if isinstance(card_data, HpsCreditCard):
                self.card = Card(card_data.number,
                                 card_data.cvv,
                                 card_data.exp_month,
                                 card_data.exp_year)
            else:
                self.card = Card(card_data, cvc, exp_month, exp_year)

    @classmethod
    def from_dict(cls, data):
        token = cls()
        for key in data:
            if key == "card":
                token.card = Card.from_dict(data[key])
            elif key == "error":
                token.error = HpsError.from_dict(data[key])
            else:
                setattr(token, key, data[key])
        return token


class Card(object):
    number = None
    cvc = None
    exp_month = None
    exp_year = None

    def __init__(self, number, cvc, exp_month, exp_year):
        self.number = number
        self.cvc = cvc
        self.exp_month = exp_month
        self.exp_year = exp_year

    @classmethod
    def from_dict(cls, data):
        card = cls(None, None, None, None)
        for key in data:
            setattr(card, key, data[key])
        return card