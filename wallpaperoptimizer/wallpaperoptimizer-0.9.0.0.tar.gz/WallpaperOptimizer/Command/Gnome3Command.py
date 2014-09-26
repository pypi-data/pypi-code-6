# -*- coding: utf-8 -*-

import subprocess

from WallpaperOptimizer.Command.Command import Command


class Gnome3Command(Command):
    def setWall(self, path):
        self.ret = subprocess.call(
            [self.command,
                "set",
                "org.gnome.desktop.background",
                "picture-uri",
                "file://" + path]
        )
        return self.ret

    def setView(self):
        self.retopt = subprocess.call(
            [self.command,
                "set",
                "org.gnome.desktop.background",
                "picture-options",
                "spanned"]
        )
        return self.retopt

    def getWall(self):
        self.current = subprocess.Popen(
            [self.command,
                "get",
                "org.gnome.desktop.background",
                "picture-uri"],
            stdout=subprocess.PIPE
        ).communicate()[0].rstrip()
        self.current.replace('file://', '')
        return self.current

    def __init__(self):
        self.command = "gsettings"
