# -*- coding: utf-8 -*-

import subprocess

from WallpaperOptimizer.Command.Command import Command


class Gnome2Command(Command):
    def setWall(self, path):
        self.ret = subprocess.call(
            [self.command,
                "--type",
                "string",
                "--set",
                "/desktop/gnome/background/picture_filename",
                path]
        )
        return self.ret

    def setView(self):
        self.retopt = subprocess.call(
            [self.command,
                "--type",
                "string",
                "--set",
                "/desktop/gnome/background/picture_options",
                "scaled"]
        )
        return self.retopt

    def getWall(self):
        self.current = subprocess.Popen(
            [self.command,
                "--get",
                "/desktop/gnome/background/picture_filename"],
            stdout=subprocess.PIPE
        ).communicate()[0].rstrip()
        return self.current

    def __init__(self):
        self.command = "gconftool-2"
