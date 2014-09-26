# -*- coding: utf-8 -*-

import pygtk

pygtk.require("2.0")
import gtk

from WallpaperOptimizer.Widget.DialogBase import DialogBase


class SaveWallpaperDialog(DialogBase):
    def btnOpen_clicked(self, widget):
        self.Dialog.response(gtk.RESPONSE_OK)

    def btnOk_clicked(self, widget):
        pass

    def openDialog(self):
        self.Dialog.show_all()
        result = self.Dialog.run()
        if result == gtk.RESPONSE_OK:
            savefilename = self.Dialog.get_filename()
        else:
            savefilename = None
        self.Dialog.destroy()
        return savefilename

    def __init__(self, gladefile):
        (self.walkTree, self.Dialog) = \
            self.loadGladeTree(gladefile, "SaveWallpaperDialog")

        dic = {
            "on_btnOpen_clicked": self.btnOpen_clicked,
            "on_btnCancel_clicked": self.btnCancel_clicked,
            "on_SaveWallpaperDialog_destroy": self.btnCancel_clicked
        }
        self.walkTree.signal_autoconnect(dic)
