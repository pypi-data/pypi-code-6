# -*- coding: utf-8 -*-

import pygtk

pygtk.require("2.0")
import gtk

from WallpaperOptimizer.Widget.DialogBase import DialogBase


class ColorSelectionDialog(DialogBase):
    def openDialog(self, bgcolor):
        self.Dialog.show_all()
        #gdkColor = gtk.gdk.Color()
        gdkColor = gtk.color_selection_palette_from_string(bgcolor)
        self.walkTree.get_widget(
            'color_selection').set_current_color(gdkColor[0])
        result = self.Dialog.run()
        if result == gtk.RESPONSE_OK:
            gtkColor = self.walkTree.get_widget(
                'color_selection').get_current_color()
            bgcolor = gtk.color_selection_palette_to_string([gtkColor])
        self.Dialog.destroy()
        return bgcolor

    def __init__(self, gladefile):
        (self.walkTree, self.Dialog) = self.loadGladeTree(
            gladefile,
            "ColorSelectionDialog")

        dic = {
            "on_btnOk_clicked": self.btnOk_clicked,
            "on_btnCancel_clicked": self.btnCancel_clicked,
            "on_ColorSelectionDialog_destroy": self.btnCancel_clicked,
        }
        self.walkTree.signal_autoconnect(dic)
