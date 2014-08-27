#!/usr/bin/env python

from GtkApp import *

class ColorSelector(GtkApp_Toplevel):

      """
      A simple graphical tool to allow quick and easy
      selection of a color.
      """

      def __init__(this):
            GtkApp_Toplevel.__init__(this)
            this.window.set_title("Choose A Color")
            this.window.set_border_width(10)
            vbox = gtk.VBox(False, 0)
            colorsel = gtk.ColorSelection()
            button_box = gtk.HButtonBox()
            button_box.set_layout(gtk.BUTTONBOX_END)
            close_button = gtk.Button(stock = gtk.STOCK_CLOSE)
            close_button.connect("clicked", gtk.main_quit)
            button_box.pack_end(close_button, False, False, 0)
            vbox.pack_start(colorsel, False, False, 0)
            vbox.pack_start(button_box, False, False, 0)
            this.window.add(vbox)
            this.window.show_all()

if __name__ == "__main__": ColorSelector().main()
