# -*- coding: utf-8 -*-

import pygtk

pygtk.require("2.0")
import gtk

from WallpaperOptimizer.Glade import Glade


class DialogBase(object):
    def btnOk_clicked(self, widget):
        self.Dialog.response(gtk.RESPONSE_OK)

    def btnCancel_clicked(self, widget):
        self.Dialog.response(gtk.RESPONSE_CANCEL)

    def loadGladeTree(self, gladefile, name):
        walkTree = Glade(gladefile, name)
        return (walkTree, walkTree.get_widget(name))
