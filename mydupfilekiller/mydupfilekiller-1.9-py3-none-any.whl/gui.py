__all__ = ["gui"]
from tkinter.messagebox import *
import time
import threading
import os
import sys
from mydupfilekiller.core import *
from mydupfilekiller.exceptions import *

gui = None
try:
    import wx
    from wx import xrc

    def call_and_wait(target, *args, **kwargs):
        if wx.IsMainThread():
            return target(*args, **kwargs)
        else:
            context = dict()
            context['event'] = threading.Event()
            wx.CallAfter(call_in_main_thread, context, target, *args, **kwargs)
            context['event'].wait()
            if 'exception' in context:
                raise SkipAllException()
            return context['result']

    def call_in_main_thread(context, target, *args, **kwargs):
        try:
            context['result'] = target(*args, **kwargs)
        except:
            context['exception'] = True
        context['event'].set()

    def main_thread(func, *args, **kwargs):
        def _func(*args, **kwargs):
            return call_and_wait(func, *args, **kwargs)
        return _func

    def get_path(path):
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), path)

    class App(wx.App):

        def OnInit(self):
            self.res = xrc.XmlResource(get_path('wx_gui.xrc'))
            self.init_frame()
            return True

        def init_frame(self):
            self.frame = self.res.LoadFrame(None, 'MainFrame')
            self.frame.SetSize((800, 600))
            self.path = xrc.XRCCTRL(self.frame, 'path')
            self.add = xrc.XRCCTRL(self.frame, 'add')
            self.delete = xrc.XRCCTRL(self.frame, 'delete')
            self.list = xrc.XRCCTRL(self.frame, 'paths')
            self.skip_empty_files = xrc.XRCCTRL(self.frame, 'skip_empty_files')
            self.follow_links = xrc.XRCCTRL(self.frame, 'follow_links')
            self.start = xrc.XRCCTRL(self.frame, 'start')
            self.status_bar = xrc.XRCCTRL(self.frame, 'status_bar')

            self.status_bar.SetFieldsCount(1)
            self.status_bar.SetStatusWidths([-1])
            self.status_bar.SetStatusText("Ready.")

            self.add.Bind(wx.EVT_BUTTON, self.OnAdd)
            self.start.Bind(wx.EVT_BUTTON, self.OnStart)
            self.delete.Bind(wx.EVT_BUTTON, self.OnDelete)

            self.skip_empty_files.SetValue(True)

            self.frame.Show()
            self.paths = []

            self.frame.Bind(wx.EVT_CLOSE, self.OnClose)

        def OnClose(self, event):
            self.Destroy()
            sys.exit()

        def OnDelete(self, event):
            selections = list(self.list.GetSelections())
            selections.reverse()
            for index in selections:
                self.list.Delete(index)
                self.paths.pop(index)

        def OnAdd(self, event):
            path = self.path.GetPath()
            path = os.path.abspath(path)
            if (not os.path.exists(path)) or (not os.path.isdir(path)):
                wx.MessageBox("Wrong path!",
                              "My Duplicate File Killer", wx.OK | wx.ICON_ERROR)
                return
            if path in self.paths:
                wx.MessageBox("Path already exists!",
                              "My Duplicate File Killer", wx.OK | wx.ICON_ERROR)
                return
            self.paths.append(path)
            self.list.Append(path)

        def OnStart(self, event):
            self.start.Disable()
            threading.Thread(target=self.timing_function).start()
            threading.Thread(target=self.working_function).start()

        def timing_function(self):
            times = 0
            while not self.start.IsEnabled():
                self.status_bar.SetStatusText("Finding" + '.' * times)
                times += 1
                times %= 10
                time.sleep(1)
            self.status_bar.SetStatusText("Ready.")

        def working_function(self):
            find_and_delete(self.paths, self.choose_callback,
                            False, self.skip_empty_files.GetValue(), self.follow_links.GetValue())
            self.start.Enable()

        @main_thread
        def choose_callback(self, files):
            print(files)
            self.dialog = self.res.LoadDialog(None, 'ChooseDialog')
            self.dialog_list = xrc.XRCCTRL(self.dialog, 'list')
            self.dialog_delete = xrc.XRCCTRL(self.dialog, 'delete')
            self.dialog_skip = xrc.XRCCTRL(self.dialog, 'skip')
            self.dialog_skip_all = xrc.XRCCTRL(self.dialog, 'skip_all')
            self.dialog_list.Clear()
            for path in files:
                self.dialog_list.Append(path)
            self.dialog.Bind(wx.EVT_CLOSE, self.OnDialogSkip)
            self.dialog_skip.Bind(wx.EVT_BUTTON, self.OnDialogSkip)
            self.dialog_delete.Bind(wx.EVT_BUTTON, self.OnDialogDelete)
            self.dialog_skip_all.Bind(wx.EVT_BUTTON, self.OnDialogSkipAll)
            self.result = set()
            self.raise_exception = False
            self.dialog.ShowModal()
            if self.raise_exception:
                raise SkipAllException()
            return self.result

        def OnDialogSkip(self, event):
            self.dialog.Destroy()

        def OnDialogDelete(self, event):
            self.result = set(self.list.GetSelections())
            self.dialog.Destroy()

        def OnDialogSkipAll(self, event):
            self.raise_exception = True
            self.dialog.Destroy()

    def wx_gui():
        app = App()
        app.MainLoop()

    gui = wx_gui
except ImportError:
    wx = None
    xrc = None

    def require_wx():
        showerror("My Duplicate File Killer",
                  "No wxPython-Phoenix installed. Please type pip install --pre -f \
                http://wxpython.org/Phoenix/snapshot-builds wxpython-phoenix --upgrade.")
    gui = require_wx
