# -*- coding: utf-8 -*-

import pygtk

pygtk.require("2.0")
import gtk

from WallpaperOptimizer.Widget.DialogBase import DialogBase


class ErrorDialog(DialogBase):
    def btnCancel_clicked(self, widget):
        pass

    def openDialog(self, msg):
        self.Dialog.show_all()
        self.walkTree.get_widget('tviewError').get_buffer().set_text(msg)
        result = self.Dialog.run()
        if result == gtk.RESPONSE_OK:
            self.Dialog.destroy()
        else:
            self.Dialog.destroy()

    def __init__(self, gladefile):
        (self.walkTree, self.Dialog) = \
            self.loadGladeTree(gladefile, "ErrorDialog")

        dic = {
            "on_btnOk_clicked": self.btnOk_clicked,
            "on_ErrorDialog_destroy": self.btnCancel_clicked
        }
        self.walkTree.signal_autoconnect(dic)
