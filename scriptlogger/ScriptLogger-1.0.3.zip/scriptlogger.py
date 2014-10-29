#    Logger - Simple Logging for scripts and terminal based programs
#    Created by FourOhFour: 404.FourOhFour@gmail.com

import time
from enum import Enum

class LogType(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2
    FATAL = 3
    FAILURE = 4
    SUCCESS = 5
    STARTING = 6
    COMPLETE = 7
    WAITING = 8
    ABOUT = 9
    

class Logger:
    def __init__(self, autoprint, header, timeformat = None):
        assert(isinstance(autoprint, bool))
        if timeformat == None:
            self.tf = "%H:%M:%S"
        else:
            self.tf = timeformat
        
        self.ap = autoprint
        self.l = [header]
        self.pointer = 0

        if autoprint:
            print(self.l[0])

    def log(self, ltype, logtext):
        tnow = time.strftime(self.tf)

        tolog = "[" + tnow + " " + ltype.name.replace("_", " ") + "] " + logtext
        self.l.append(tolog)
        if self.ap:
            print(tolog)

    def getNew(self):
        return self.l[self.pointer:]
        self.pointer = len(self.l)

    def printNew(self):
        for i in self.l[self.pointer:]:
            print(i)
        self.pointer = len(self.l)

    def getAll(self):
        return self.l

    def printAll(self):
        for i in self.l:
            print(i)
    
    def writeAllToFile(self, path):
        with open(path, "a") as f:
            for i in self.l:
                f.write(i)

    def setPointer(self, p):
        self.pointer = p
        if self.pointer < 0:
            self.pointer = 0
            
        if self.pointer > len(self.l):
            self.pointer = len(self.l)
    
    def getPointer(self):
        return self.pointer
            
        if self.pointer > len(self.l):
            self.pointer = len(self.l)

    def incrementPointer(self, amount = 1):
        self.pointer += amount
        
        if self.pointer > len(self.l):
            self.pointer = len(self.l)

    def decrementPointer(self, amount = 1):
        self.pointer -= amount
        if self.pointer < 0:
            self.pointer = 0

    def setPointerToStart(self):
        self.pointer = 0
            
    def setPointerToEnd(self):
        self.pointer = len(self.l)
