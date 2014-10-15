from numpy import array
from numpy.random import randint

from ..environment import Environment


class Discrete1dProgress(Environment):
    def __init__(self, m_card, s_card):
        Environment.__init__(self, [0.], [m_card], [0.], [s_card])

        self.m_card = m_card
        self.s_card = s_card
        self.writable = [0]
        self.readable = [0, 1]

    def compute_motor_command(self, m):
        return m

    def compute_sensori_effect(self, ag_state):
        m = ag_state[0]

        # if m == 0:
        #     s = 2
        # elif m == 1:
        #     s = m
        # elif m == 2:
        #     s = randint(2)

        if m == 0:
            s = 0
        elif m == 1:
            s = randint(2)
        elif m <= 4:
            s = 2
        elif m == 5:
            s = 3
        elif m == 6:
            s = randint(2) + 4

        return array([s])
