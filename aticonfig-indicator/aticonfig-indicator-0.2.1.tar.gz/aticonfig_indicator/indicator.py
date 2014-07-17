#!/usr/bin/env python

import sys
import gtk
import appindicator
import utils


class AticonfigIndicator(object):
    def __init__(self):
        self.ind = appindicator.Indicator("aticonfig-indicator", "aticonfig-icon",
                                          appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)

        # self.ind.set_attention_icon("ubuntu-client-error")
        #self.ind.set_label("FooBar")
        # self.ind.set_icon()

        self.menu_setup()
        self.ind.set_menu(self.menu)


    def menu_setup(self):
        self.menu = gtk.Menu()

        self.quit_item = gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)

    def main(self):
        self.check_temp()
        gtk.timeout_add(5000, self.check_temp)
        gtk.main()

    def quit(self, widget):
        sys.exit(0)

    def check_temp(self):
        # self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_status(appindicator.STATUS_ATTENTION)

        # r = str(random.randint(1, 50))
        r = utils.get_temp()

        self.ind.set_label(r)

        return True