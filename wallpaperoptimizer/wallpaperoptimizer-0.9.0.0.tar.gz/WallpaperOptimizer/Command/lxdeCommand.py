# -*- coding: utf-8 -*-

import subprocess
import os
import os.path

import WallpaperOptimizer
from WallpaperOptimizer.Command.Command import Command


class lxdeCommand(Command):
    def setWall(self, path):
        self.ret = subprocess.call(
            [self.command,
                "--set-wallpaper",
                path]
        )
        return self.ret

    def setView(self):
        self.retopt = subprocess.call(
            [self.command,
                "--wallpaper-mode=tile"]
        )
        return self.retopt

    def getWall(self):
        retpath = ""
        for (root, dirs, files) in os.walk(WallpaperOptimizer.USERENVDIR):
            for f in files:
                if f[-4:] == ".jpg":
                    return os.path.join(root, f)
        return retpath

    def __init__(self):
        self.command = "pcmanfm"
