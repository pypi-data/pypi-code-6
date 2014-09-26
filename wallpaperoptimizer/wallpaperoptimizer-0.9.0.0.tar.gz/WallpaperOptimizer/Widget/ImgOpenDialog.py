# -*- coding: utf-8 -*-

import pwd
import os.path

import pygtk

pygtk.require("2.0")
import gtk

from WallpaperOptimizer.Widget.DialogBase import DialogBase


class ImgOpenDialog(DialogBase):
    def btnOpen_clicked(self, widget):
        self.Dialog.response(gtk.RESPONSE_OK)

    def btnOk_clicked(self, widget):
        pass

    def openDialog(self, path, addlr):
        if path == '':
            self.Dialog.set_filename(
                os.path.expanduser(
                    os.path.join('~/', pwd.getpwuid(os.getuid())[0])
                ))
        else:
            self.Dialog.set_filename(os.path.abspath(path))
        self.Dialog.set_title(self.Dialog.get_title() + '(' + addlr + ')')
        self.Dialog.show_all()
        result = self.Dialog.run()
        if result == gtk.RESPONSE_OK:
            imgfilepath = self.Dialog.get_filename()
            self.Dialog.destroy()
            return imgfilepath
        else:
            self.Dialog.destroy()
            return False

    def __init__(self, gladefile):
        (self.walkTree, self.Dialog) = \
            self.loadGladeTree(gladefile, "ImgOpenDialog")
        imgFilter = gtk.FileFilter()
        imgFilter.set_name(u"画像")
        # Changer的には、この４つ
        imgFilter.add_mime_type("image/png")
        imgFilter.add_mime_type("image/jpeg")
        imgFilter.add_mime_type("image/bmp")
        imgFilter.add_mime_type("image/gif")
        imgFilter.add_pattern("*.png")
        imgFilter.add_pattern("*.jpeg")
        imgFilter.add_pattern("*.jpg")
        imgFilter.add_pattern("*.bmp")
        imgFilter.add_pattern("*.gif")
        self.Dialog.add_filter(imgFilter)
        allFile = gtk.FileFilter()
        allFile.set_name(u"全て")
        allFile.add_pattern("*")
        self.Dialog.add_filter(allFile)

        dic = {
            "on_btnOpen_clicked": self.btnOpen_clicked,
            "on_btnCancel_clicked": self.btnCancel_clicked,
            "on_ImgOpenDialog_destroy": self.btnCancel_clicked
        }
        self.walkTree.signal_autoconnect(dic)
