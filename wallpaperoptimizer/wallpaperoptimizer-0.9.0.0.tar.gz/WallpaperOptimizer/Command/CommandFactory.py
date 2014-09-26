# -*- coding: utf-8 -*-

from WallpaperOptimizer.Command.Gnome2Command import Gnome2Command
from WallpaperOptimizer.Command.Gnome3Command import Gnome3Command
from WallpaperOptimizer.Command.Xfce40Command import Xfce40Command
from WallpaperOptimizer.Command.Xfce41Command import Xfce41Command
from WallpaperOptimizer.Command.lxdeCommand import lxdeCommand


class CommandFactory(object):
    def _createCommand(self, windowmanager):
        if windowmanager == 'Gnome2':
            return Gnome2Command()
        elif windowmanager == 'Gnome3':
            return Gnome3Command()
        elif windowmanager == 'xfce40':
            return Xfce40Command()
        elif windowmanager == 'xfce41':
            return Xfce41Command()
        elif windowmanager == 'lxde':
            return lxdeCommand()

    def create(self, windowmanager):
        cmd = self._createCommand(windowmanager)
        return cmd
