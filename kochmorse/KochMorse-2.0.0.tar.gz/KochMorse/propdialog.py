from gi.repository import Gtk
import os.path
from .conffile import Config
from .alsamorse import KochLesson

class PropertyDialog:
    def __init__(self):
        self.__gladefile = os.path.join(os.path.dirname(__file__), "propdialog.ui")
        self.__xml = Gtk.Builder()
        self.__xml.add_from_file(self.__gladefile)
        self.__widget = self.__xml.get_object("propdialog")
        self.__lessontime = self.__xml.get_object("lessontime")
        self.__countdown  = self.__xml.get_object("countdown")
        self.__prefer_last = self.__xml.get_object("prefer_last")
        self.__ign_box = self.__xml.get_object("ignorechars")
        
        cfg = Config()
        self.__lessontime.set_value(cfg.opt_lessontime)
        self.__countdown.set_value(cfg.opt_countdown)
        self.__prefer_last.set_active(cfg.opt_preferlast)
        self.__ign_box.set_text(cfg.opt_ignorechars)
        
            

    def run(self):
        if self.__widget.run() == Gtk.ResponseType.CANCEL:
            self.__widget.destroy()
            return None

        cfg = Config()
        cfg.opt_lessontime  = self.__lessontime.get_value()
        cfg.opt_countdown   = self.__countdown.get_value()
        cfg.opt_preferlast  = self.__prefer_last.get_active()
        cfg.opt_ignorechars = filter(lambda x: x in KochLesson.chars,
                                     self.__ign_box.get_text())
        cfg.save()

        self.__widget.destroy()

                

