# -*- coding: utf-8 -*-

"""This module contains the Monster and Move classes."""
import json
import hashlib
try:
    from global_vars import *
except ImportError:
    from federated_monsters.global_vars import *


class Monster(object):

    """A class for the monster.

    Attributes:
        name (str): The name of the monster.
        uuid (str): A UUID associated with the monster.
        type_name (str): What elemental type the monster is.
        moves (list of Move): The instances of the Move class that can be used.
    """

    def __init__(self, name, uuid, type_name, moves):
        """Init Monster with name, uuid, type_name, moves."""
        self.name = name
        self.uuid = uuid
        self.type_name = type_name
        self.moves = moves

    def export_monster(self):
        """Export the monster to be sent to a box.

        Returns:
            tuple (hashlib.hash, str): The hash and JSON form of the monster.
        """
        tmp_dict = self.__dict__
        moves_arr = []
        for i in tmp_dict["moves"]:
            moves_arr.append(i.serialize())
        tmp_dict["moves"] = moves_arr
        txt = json.dumps(tmp_dict)
        hash_obj = hashlib.sha512(txt.encode(ENC_)).hexdigest()

        return (hash_obj, txt)


class Move(object):

    """A class for moves.

    Moves can be used by monsters in battle.

    Attributes:
        name (str): A string indicating the name of the move.
        type_name (str): What elemental type the move is.
        effect (str): What the move does.
        dmg (int): How powerful the move is
    """

    def __init__(self, name, type_name, effect, dmg):
        """Init Move with name, type_name, effect, dmg."""
        self.name = name
        self.type_name = type_name
        self.effect = effect
        self.dmg = dmg

    def serialize(self):
        """Serialize the move for storage.

        Returns:
            str: The JSON serialization of the __dict__.
        """
        return json.dumps(self, default=lambda o: o.__dict__)
