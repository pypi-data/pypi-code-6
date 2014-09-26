# -*- coding: utf-8 -*-

""" WallpaperOptimizer::Applet

wallpaperoptimizer Applet module.
"""
import sys
import os.path

import pygtk

pygtk.require("2.0")
import gtk

try:
    import glib as glibobj
except:
    try:
        import gobject as glibobj
    except:
        sys.exit(2)
try:
    import gnome.ui
except:
    print 'not installed Python bindings for the GNOME desktop environment'
    print 'ex) sudo apt-get install python-gnome2'
    print 'ex) sudo yum install python-gnome2-gnome'
    sys.exit(2)

import WallpaperOptimizer

from WallpaperOptimizer.WindowBase import WindowBase
from WallpaperOptimizer.Core import Core
from WallpaperOptimizer.OptionsBase import OptionsBase


class AppletOptions(OptionsBase):
    class Opts(object):
        def __init__(self):
            self.align = ['center', 'center']
            self.valign = ['middle', 'middle']
            self.mergin = [0, 0, 0, 0]
            self.fixed = True
            self.size = [None, None]
            self.bgcolor = 'black'
            self.srcdir = ['', '']
            self.verbose = False
            self.save = None
            self.setWall = False
            self.daemonize = False
            self.interval = 60
            self.combine = True

    def getWindow(self):
        return True

    def __init__(self):
        OptionsBase.__init__(self)
        self.opts = AppletOptions.Opts()
        self.args = ['', '']


class Applet(WindowBase):

# 	override
    def btnDaemonize_clicked(self, widget):
        self.window.hide()
        self.window.set_icon(self._select_icon(self.bCanceled))
        self.btnOnTooltip.set_text('changer on')
        self.bCanceled = False
        self.bVisible = False
        self._setPanelButton(self.applet, self.bCanceled)
        self._switchWidget(False)
        self.timeoutObject = glibobj.timeout_add(
            self.option.opts.interval * 1000,
            self._timeout, self)
        self.logging.debug(
            '%20s' %
            'Start Daemonize ... interval [%d].' %
            self.option.opts.interval)
        self._runChanger()

    # 	override
    def btnCancelDaemonize_clicked(self, widget):
        self.bCanceled = True
        self._setPanelButton(self.applet, self.bCanceled)
        self.window.set_icon(self._select_icon(self.bCanceled))
        self.btnOnTooltip.set_text('changer off')
        glibobj.source_remove(self.timeoutObject)
        self.timeoutObject = None
        self._writeStatusbar(
            self.statbar, self.cid_stat, 'Cancel ... changer action.')
        self._switchWidget(True)

    def btnAbout_clicked(self, widget):
        icon = self._select_icon(self.bCanceled)
        about = gnome.ui.About(
            "WallpaperOptimizer",
            WallpaperOptimizer.VERSION,  # version
            "GPLv3",  # copyright
            "wallpaperoptimizer is multi wallpaper changer.",  # comments
            [WallpaperOptimizer.AUTHOR],  # **authors
            [WallpaperOptimizer.AUTHOR],  # **documenters
            WallpaperOptimizer.AUTHOR,  # *translator_credits
            icon)            # gtk.gdk.Pixbuf
        about.show_all()

    # panel control group
    def _select_icon(self, bCanceled):
        if bCanceled:
            icon = self.dis_icon
        else:
            icon = self.ena_icon
        return icon

    def _preferences(self, *arguments):
        self.btnSetting_clicked(None)

    def _selectColor(self, *arguments):
        self.btnSetColor_clicked(None)

    def _about(self, *arguments):
        self.btnAbout_clicked(None)

    def _create_menu(self, applet):
        menuxml = """
            <popup name="button3">
                 <menuitem
                    name="Item 2"
                    verb="Visible"
                    label="Visible／Invisible"
                    pixtype="stock"
                    pixname="gtk-execute"/>
                 <menuitem
                    name="Item 3"
                    verb="Preferences"
                    label="Settings"
                    pixtype="stock"
                    pixname="gtk-preferences"/>
                 <menuitem
                    name="Item 4"
                    verb="Color"
                    label="BaseColor"
                    pixtype="stock"
                    pixname="gtk-select-color"/>
                 <menuitem
                    name="Item 5"
                    verb="About"
                    label="About"
                    pixtype="stock"
                    pixname="gtk-about"/>
            </popup>"""
        #
        verbs = [("Visible", self._visibleCtrl),
                 ("Preferences", self._preferences),
                 ("Color", self._selectColor),
                 ("About", self._about)]
        applet.setup_menu(menuxml, verbs, None)

    def _setMenu(self, widget, event, applet):
        if event.button == 1:
            if self.core.config.lDisplay.getBool():
                if self.bCanceled:
                    self.btnDaemonize_clicked(None)
                else:
                    self.btnCancelDaemonize_clicked(None)
            else:
                self._writeStatusbar(
                    self.statbar, self.cid_stat, 'Please set up Config.')
        elif event.button == 3:
            widget.emit_stop_by_name("button-press-event")
            self._create_menu(applet)

    def _setPanelButton(self, applet, bCanceled):
        icon = self._select_icon(bCanceled)
        icon2 = icon.scale_simple(
            icon.get_width() - 4,
            icon.get_width() - 4,
            gtk.gdk.INTERP_BILINEAR)
        iconOnPanel = gtk.Image()
        iconOnPanel.set_from_pixbuf(icon2)
        self.btnOnPanelBar.set_image(iconOnPanel)

    def _loadIcon(self):
        self.dis_icon = gtk.gdk.pixbuf_new_from_file(os.path.abspath(
            os.path.join(WallpaperOptimizer.ICONDIR, 'wallopt_off.png')))
        self.ena_icon = gtk.gdk.pixbuf_new_from_file(os.path.abspath(
            os.path.join(WallpaperOptimizer.ICONDIR, 'wallopt.png')))

    def __init__(self, applet, iid, logging):
        self.applet = applet
        self.logging = logging
        #  Initialize Status
        self.timeoutObject = None
        self.bVisible = True
        self.bCanceled = True
        self.bEntryPath = [False, False]
        # Initialize Panel
        self._loadIcon()
        self.btnOnPanelBar = gtk.Button()
        self.btnOnPanelBar.set_relief(gtk.RELIEF_NONE)
        self._setPanelButton(self.applet, self.bCanceled)
        self.btnOnPanelBar.connect(
            "button-press-event", self._setMenu, self.applet)
        self.applet.add(self.btnOnPanelBar)
        # add Tooltips
        self.btnOnTooltip = gtk.Tooltip()
        self.btnOnTooltip.set_text('changer off')
        self.applet.show_all()
        self.applet.connect("destroy", gtk.main_quit)
        # AppletOptions extends Options class
        self.option = AppletOptions()
        self.core = Core(self.option)
        # Initialize Applet
        self._initializeWindow()
