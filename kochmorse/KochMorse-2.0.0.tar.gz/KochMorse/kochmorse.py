#!/usr/bin/python

from gi.repository import GObject, Gdk, Gtk
import time 
import os.path

from . import alsamorse
from .propdialog import PropertyDialog
from .conffile import Config





class KochMorse:

    def __init__(self):
        self.__gladefile = os.path.join(os.path.dirname(__file__), "kochmorse.ui")
        self.__xml = Gtk.Builder()
        self.__xml.add_from_file(self.__gladefile)
        self.__window     = self.__xml.get_object("window1")
        self.__textview   = self.__xml.get_object("textview")
        self.__statusbar  = self.__xml.get_object("statusbar")
        self.__speedspin  = self.__xml.get_object("speedspin")
        self.__effspeed   = self.__xml.get_object("effspeedspin")
        self.__lessonspin = self.__xml.get_object("lessonspin")
        self.__freqspin   = self.__xml.get_object("freqspin")
        self.__timelabel  = self.__xml.get_object("timelabel")
        self.__playbutton = self.__xml.get_object("playbutton")
        self.__volume     = self.__xml.get_object("volume")

        # load config and set entries
        self.__config = Config()
        self.__lesson_start = None
  
        self.__speedspin.set_value(self.__config.opt_speed)
        self.__effspeed.set_range(10, self.__config.opt_speed)
        self.__effspeed.set_value(self.__config.opt_effspeed)
        self.__lessonspin.set_value(self.__config.opt_lesson)
        self.__freqspin.set_value(self.__config.opt_frequency)
        self.__volume.set_value(self.__config.opt_volume)
 
        self.__engine = alsamorse.Morse(frequency = self.__config.opt_frequency, 
                                        speed = self.__config.opt_speed, 
                                        eff_speed = self.__config.opt_effspeed, 
                                        volume = self.__config.opt_volume)
        self.__lesson = alsamorse.KochLesson(self.__config.opt_lesson, self.__config.opt_ignorechars)
        self.__engine.set_char_source(self.__lesson)
        self.__engine.set_notifier(self.on_char_send)

        self.__lessonspin.set_range(2, self.__lesson.get_num_lessons())

        self.__xml.connect_signals({
                'on_playbutton_toggled': self.on_play_toggled,
                'on_quit': self.on_quit,
                'on_info_show': self.on_info_show,
                'on_propbutton_clicked': self.on_propbutton_clicked,
                'on_volume_changed': self.on_volume_changed,
                'on_speed_changed': self.on_speed_changed,
                'on_eff_speed_changed': self.on_eff_speed_changed,
                'on_lesson_changed': self.on_lesson_changed,
                'on_freq_changed': self.on_freq_changed})

        GObject.timeout_add(500, self.on_update_time)
        

    def on_play_toggled(self, button):
        if button.get_active():
            # clear char counter and textview
            self.__lesson.reset_char_counter()
            self.__textview.get_buffer().set_text("")
            self.__lesson_start = time.time()
        else:
            self.__engine.set_pause(True)
            self.__lesson_start = None


    def on_info_show(self, button):
        info_file = os.path.join(os.path.dirname(__file__), "infodialog.ui")
        info_xml = Gtk.Builder()
        info_xml.add_from_file(info_file);
        info_dialog = info_xml.get_object("infodialog")
        info_dialog.run()
        info_dialog.destroy()

    
    def on_propbutton_clicked(self, button):
        dlg = PropertyDialog()
        dlg.run()
        self.__lesson.set_preferlast(self.__config.opt_preferlast)
        self.__lesson.set_ignore_chars(self.__config.opt_ignorechars)


    def on_quit(self, window):
        self.__engine.stop()
        Gtk.main_quit()


    def on_char_send(self, char):
        Gdk.threads_enter()
        self.__textview.get_buffer().insert_at_cursor(char)        
        self.__statusbar.push(1, "%i chars send"%self.__lesson.get_chars_send())
        Gdk.threads_leave()

    
    def on_update_time(self):
        # if playbutton is pressed:
        if self.__lesson_start:
            # calc sec since start-button clicked
            tdiff = time.time()-self.__lesson_start-self.__config.opt_countdown
            
            if tdiff < 0:
                # while countdown:
                self.__timelabel.set_markup("<tt><big><b>%5i</b></big></tt>"%(tdiff))
            else:
                # after countdown
                if self.__engine.is_paused(): self.__engine.set_pause(False)
                # get and display sec since start:
                t = self.__engine.get_time()
                self.__timelabel.set_markup("<tt><big><b>%02i:%02i</b></big></tt>"%(int(t)/60,t%60))
            
                # check if lessontime is elapsed
                if t >= self.__config.opt_lessontime*60:
                    self.__playbutton.set_active(False)

        return True    


    def on_volume_changed(self, widget):
        self.__config.opt_volume = float(widget.get_value())
        self.__engine.set_volume( widget.get_value() )
        self.__config.save()


    def on_speed_changed(self, widget):
        self.__config.opt_speed = int(widget.get_value())
        self.__engine.set_speed(widget.get_value())
        self.__effspeed.set_range(10, self.__config.opt_speed)
        
        if self.__effspeed.get_value() > self.__config.opt_speed:
            self.__effspeed.set_value(self.__config.opt_effspeed)
            
        self.__config.save()
           
 
    def on_eff_speed_changed(self, widget):
        self.__config.opt_effspeed = int(widget.get_value())
        self.__engine.set_eff_speed( widget.get_value() )
        self.__config.save()


    def on_lesson_changed(self, widget):
        self.__config.opt_lesson = int(widget.get_value())
        self.__lesson.set_lesson(widget.get_value())
        self.__config.save()


    def on_freq_changed(self, widget):    
        self.__config.opt_frequency = float(widget.get_value())
        self.__engine.set_frequency(widget.get_value())
        self.__config.save()



