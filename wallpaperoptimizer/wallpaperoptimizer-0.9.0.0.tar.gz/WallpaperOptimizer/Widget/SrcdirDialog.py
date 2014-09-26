# -*- coding: utf-8 -*-

import os.path

import pygtk

pygtk.require("2.0")
import gtk

from WallpaperOptimizer.Widget.DialogBase import DialogBase


class SrcdirDialog(DialogBase):
    def btnOpen_clicked(self, widget):
        self.Dialog.response(gtk.RESPONSE_OK)

    def btnOk_clicked(self, widget):
        pass

    def openDialog(self, srcdir, addlr):
        self.Dialog.set_title(self.Dialog.get_title() + '(' + addlr + ')')
        self.Dialog.set_current_folder(os.path.expanduser(srcdir))
        self.Dialog.show_all()
        result = self.Dialog.run()
        if result == gtk.RESPONSE_OK:
            srcdir = self.Dialog.get_current_folder()
            self.Dialog.destroy()
            return srcdir
        else:
            self.Dialog.destroy()
            return False

    def __init__(self, gladefile):
        (self.walkTree, self.Dialog) = \
            self.loadGladeTree(gladefile, "SrcdirDialog")

        dic = {
            "on_btnOpen_clicked": self.btnOpen_clicked,
            "on_btnCancel_clicked": self.btnCancel_clicked,
            "on_SrcdirDialog_destroy": self.btnCancel_clicked
        }
        self.walkTree.signal_autoconnect(dic)
