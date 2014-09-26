# -*- coding: utf-8 -*-

import sys
import gtk

from WallpaperOptimizer.Starter import Starter


class Gnome2Starter(Starter):
    def _factory(self, applet, iid):
        """
        for gnomeapplet factory method.
        """
        from WallpaperOptimizer.Applet import Applet

        Applet(applet, iid, self.logging)
        return gtk.TRUE

    def start(self, option, logging):
        self.option = option
        self.logging = logging

        try:
            import gnomeapplet
        except:
            print "not installed Python bindings for GNOME Panel applets."
            print "ex)  sudo yum install gnome-python2-applet"
            self.logging.error(
                'not installed Python bindings for GNOME Panel applets.')
            self.logging.error('ex)  sudo yum install gnome-python2-applet')
            sys.exit(2)

        if option.getWindow():
            self.logging.debug('Running ... window mode.')
            import pygtk

            pygtk.require("2.0")
            main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
            main_window.set_title("Wallpaperoptimizer Applet Window")
            main_window.connect("destroy", gtk.main_quit)
            app = gnomeapplet.Applet()
            self._factory(app, None)
            app.reparent(main_window)
            main_window.show_all()
            wh = main_window.get_size()
            main_window.resize(wh[0] * 2, wh[1])
            gtk.main()
        elif (
            option.getIID() is None and
            option.getFD() is None
        ):
            self._runConsoleSide(self.option, self.logging)

        else:
            self.logging.debug('Running ... applet mode.')
            import pygtk

            pygtk.require("2.0")
            gnomeapplet.bonobo_factory(
                "OAFIID:wallpaperoptimizerApplet_Factory",
                gnomeapplet.Applet.__gtype__,
                "wallpaper changer",
                "1.0",
                self._factory
            )
