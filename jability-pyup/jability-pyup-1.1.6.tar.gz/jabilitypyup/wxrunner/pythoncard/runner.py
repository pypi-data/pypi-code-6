"""
__version__ = "$Revision: 1.5 $"
__date__ = "$Date: 2004/04/30 16:26:12 $"
"""

import os
import signal
import subprocess
import sys
import time

try:
    import wxversion
    wxversion.select('2.8')
except ImportError as e:
    print u"python 'wxVersion' module not installed !"

try:
    import wx
except ImportError as e:
    print u"python 'wxPython' module not installed !"
    raise e

try:
    from PythonCard import model, timer
except ImportError as e:
    print u"python 'PythonCard' module not installed !"
    raise e

class MyBackground(model.Background):

    def on_initialize(self, event):
        print "on_initialize"
        self.pid = None
        self.txtbuffer=""
        self.components.textConsole.SetStyle(0,1, wx.TextAttr("WHITE","BLACK"))
        #self.myTimer = timer.Timer(self.components.textConsole, -1)
        self.myTimer2 = timer.Timer(self.components.textConsole, -1)
        self.myTimer2.Start(2000)
        #self.myTimer.Start(5000)
        self.on_size(event)

    def on_size(self, event):
        print "on_size"
        self.panel.size = ( self.size[0], self.size[1])
        self.components.textConsole.size = (self.size[0]-20, self.size[1]-105)
        self.panel.Layout()

    def on_ToggleButton_mouseClick(self, event):
        print "on/off :" + str(self.components.ToggleButton.checked)
        if self.components.ToggleButton.checked:
            if self.pid is None:
                self.start_process()
        else:
            if self.pid is not None:
                self.stop_process()

    #def on_textConsole_timer(self, event):
     #   if not self.txtbuffer == "":
      #      print self.txtbuffer
       #     self.components.textConsole.appendText(self.txtbuffer)
        #    self.txtbuffer=""

    def on_cbDebug_mouseClick(self, event):
        print "debug on/off"

    def on_textConsole_timer(self, event):
        if self.pid is not None:
            retcode = self.pid.poll()
            if retcode is None:
                self.pid.stdout.flush()
                char = self.pid.stdout.read(1)
                while char:
                    self.txtbuffer += char
                    #if char == '\n':
                    self.components.textConsole.appendText(str(self.txtbuffer))
                    self.txtbuffer=""
                    char = self.pid.stdout.read(1)
            else:
                self.pid.stdout.flush()
                char = self.pid.stdout.read(1)
                while char:
                    self.txtbuffer += char
                    #if char == '\n':
                    self.components.textConsole.appendText(str(self.txtbuffer))
                    self.txtbuffer=""
                    char = self.pid.stdout.read(1)
                    self.pid=None


    def start_process(self):
        self.txtbuffer=""
        self.pid = subprocess.Popen(    "python ijgHL7ADT.py -d",
                                        shell=True,
                                        stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        #stdout, stderr = self.pid.communicate()

    def stop_process(self):
        if self.pid is not None:
            os.kill(self.pid,signal.SIGTERM)
            time.sleep(1)
            if self.pid.poll() is None:
                os.kill(self.pid,signal.SIGKILL)
            self.pid = None
            self.components.textConsole.appendText(str(self.txtbuffer))
            self.txtbuffer=""


if __name__ == '__main__':
    app = model.Application(MyBackground)
    app.MainLoop()
