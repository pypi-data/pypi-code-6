# -*- coding: utf-8 -*-
from .commandmanager import CommandManager
from .textmanager import TextManager


def search(mask_str, dt):
    text_manager = TextManager(dt)
    command_manager = CommandManager(mask_str, text_manager=text_manager)
    return text_manager.execute(command_manager=command_manager)
