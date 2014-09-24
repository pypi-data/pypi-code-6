# -*- coding: utf-8 -*-

from objectpack.demo import controller

import actions


def register_actions():
    controller.action_controller.packs.append(actions.Pack())
