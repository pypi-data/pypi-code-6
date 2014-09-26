# -*- coding: utf-8 -*-

import gtk

from WallpaperOptimizer.Starter import Starter


class Gnome3Starter(Starter):
    def start(self, option, logging):
        self.option = option
        self.logging = logging

        if (
            option.getSavePath() is None and
            option.getSetWall() is False and
            option.getWindow() is False and
            option.getDaemonize() is False
        ):
            import gobject

            gobject.set_application_name('wallpaperoptimizer')
            gobject.set_prgname('wallpaperoptimizer')

            from WallpaperOptimizer.AppIndicator import AppIndicator

            AppIndicator(self.option, self.logging)
            gtk.main()
        else:
            self._runConsoleSide(self.option, self.logging)
