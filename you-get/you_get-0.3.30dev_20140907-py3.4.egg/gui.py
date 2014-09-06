#!/usr/bin/env python

import tkinter

class Application(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.hi_there = tkinter.Button(self)
        self.hi_there["text"] = "You-Get\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.QUIT = tkinter.Button(self, text="QUIT", fg="red",
            command=root.destroy)
        self.QUIT.pack(side="bottom")

    def say_hi(self):
        print("you-get is running!")

root = tkinter.Tk()
def gui_main(*args, **conf):
    from .console import console_main#
    console_main(*args, **conf)#

    app = Application(master=root)
    app.mainloop()
