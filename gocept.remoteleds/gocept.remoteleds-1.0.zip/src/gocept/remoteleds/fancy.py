from .client import Client
import random


class FancyClient(Client):

    update_ticks = 3
    support_state_changes = False

    def __init__(self, *arg, **kw):
        super(FancyClient, self).__init__(*arg, **kw)

    def get_state_for_project(self, project):
        if random.randint(0,4) == 0:
            return (random.randint(0,255),
                    random.randint(0,255),
                    random.randint(0,255))
        else:
            return (0,0,0)


    def get_color_for_state(self, state):
        r, g, b = state
        return r, g, b

    def get_sound_for_state(self, state):
        return
