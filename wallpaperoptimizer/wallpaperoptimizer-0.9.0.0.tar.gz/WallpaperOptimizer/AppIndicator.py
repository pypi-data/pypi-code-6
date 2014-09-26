# -*- coding: utf-8 -*-

""" WallpaperOptimizer::AppIndicator

wallpaperoptimizer AppIndicator module.
"""

import sys
import os.path
import pygtk

pygtk.require("2.0")
import gtk

try:
    import glib as glibobj
    # Ubuntuでは活きた
except:
    try:
        import gobject as glibobj
    except:
        sys.exit(2)

try:
    import appindicator
except:
    print 'not installed Python bindings for libappindicator'
    print 'ex) sudo apt-get install python-appindicator'
    sys.exit(2)

import WallpaperOptimizer

from WallpaperOptimizer.WindowBase import WindowBase
from WallpaperOptimizer.Core import Core


class AppIndicator(WindowBase):
    def quit(self, widget):
        sys.exit(0)

    def _create_menu(self):
        self.indicatormenu = gtk.Menu()

        self.visible_item = gtk.MenuItem("Visible/Invisible")
        self.preference_item = gtk.MenuItem("Settings")
        self.color_item = gtk.MenuItem("BaseColor")
        self.about_item = gtk.MenuItem("About")
        self.quit_item = gtk.MenuItem("Quit")

        self.visible_item.connect("activate", self._visibleCtrl)
        self.preference_item.connect("activate", self._preferences)
        self.color_item.connect("activate", self._selectColor)
        self.about_item.connect("activate", self._about)
        self.quit_item.connect("activate", self.quit)

        self.visible_item.show()
        self.preference_item.show()
        self.color_item.show()
        self.about_item.show()
        self.quit_item.show()

        self.indicatormenu.append(self.visible_item)
        self.indicatormenu.append(self.preference_item)
        self.indicatormenu.append(self.color_item)
        self.indicatormenu.append(self.about_item)
        self.indicatormenu.append(self.quit_item)

    def btnDaemonize_clicked(self, widget):
        self.window.hide()
        self.window.set_icon(self._select_icon(self.bCanceled))
        self.bCanceled = False
        self.bVisible = False
        self.indicator.set_icon('wallopt')
        self._switchWidget(False)
        self.timeoutObject = glibobj.timeout_add(
            self.option.opts.interval * 1000, self._timeout, self)
        self.logging.debug(
            '%20s' %
            'Start Daemonize ... interval [%d].' %
            self.option.opts.interval)
        self._runChanger()

    def btnCancelDaemonize_clicked(self, widget):
        self.bCanceled = True
        self.indicator.set_icon('wallopt_off')
        self.window.set_icon(self._select_icon(self.bCanceled))
        glibobj.source_remove(self.timeoutObject)
        self.timeoutObject = None
        self._writeStatusbar(
            self.statbar, self.cid_stat, 'Cancel ... changer action.')
        self._switchWidget(True)

    def _setEmail(self, email):
        gtk.show_uri(None, "mailto:%s" % email, gtk.gdk.CURRENT_TIME)

    def _setUrl(self, link):
        gtk.show_uri(None, link, gtk.gdk.CURRENT_TIME)

    def _aboutDialog_destroy(self, dialog, response):
        dialog.destroy()

    def btnAbout_clicked(self, widget):
        icon = self._select_icon(self.bCanceled)
        about = gtk.AboutDialog()
        about.set_name('WallpaperOptimizer')
        about.set_logo(icon)  # gtk.gdk.Pixbuf
        #		about.set_license('GPLv3')
        about.set_copyright('Copyright @ 2012-2013 Katsuhiro Ogikubo')
        about.set_comments('wallpaperoptimizer is multi wallpaper changer.')
        about.set_version(WallpaperOptimizer.VERSION)
        about.set_authors([WallpaperOptimizer.AUTHOR])
        about.set_documenters([WallpaperOptimizer.AUTHOR])
        about.set_translator_credits(WallpaperOptimizer.AUTHOR)
        about.set_website('http://oggy.no-ip.info/blog/software/')
        about.set_website_label('WallpaperOptimizer page')
        about.connect("response", self._aboutDialog_destroy)
        about.show_all()

    gtk.about_dialog_set_email_hook(_setEmail)
    gtk.about_dialog_set_url_hook(_setUrl)

    def _select_icon(self, bCanceled):
        if bCanceled:
            icon = self.dis_icon
        else:
            icon = self.ena_icon
        return icon

    def _loadIcon(self):
        self.dis_icon = gtk.gdk.pixbuf_new_from_file(os.path.abspath(
            os.path.join(
                self.indicator.get_icon_theme_path(),
                'wallopt_off.png')))
        self.ena_icon = gtk.gdk.pixbuf_new_from_file(os.path.abspath(
            os.path.join(
                self.indicator.get_icon_theme_path(),
                'wallopt.png')))

    def __init__(self, option, logging):
        # id, icon_name, category, icon_theme_path
        self.indicator = appindicator.Indicator(
            'WallpaperOptimzier',
            "wallopt_off",
            appindicator.CATEGORY_APPLICATION_STATUS,
            WallpaperOptimizer.ICONDIR)
        self.option = option
        self.logging = logging

        #  Initialize Status
        self.timeoutObject = None
        self.bVisible = True
        self.bCanceled = True
        self.bEntryPath = [False, False]

        #  Initialize AppIndicator
        self._loadIcon()
        self.indicator.set_status(appindicator.STATUS_ACTIVE)
        self._create_menu()
        self.indicator.set_menu(self.indicatormenu)
        gtk.window_set_default_icon(self._select_icon(self.bCanceled))

        self.indicator.set_icon('wallopt')

        #  optionInitialize
        self.option.opts.window = True
        self.option.args = ['', '']
        self.core = Core(self.option)

        #  Initialize Applet
        self._initializeWindow()
