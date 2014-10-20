import os
import shutil
import cProfile

from spelltinkle.exceptions import StopSession
from spelltinkle.run import run
from spelltinkle.session import Session
from spelltinkle.test.tests import all_tests
import spelltinkle.test.tests as tests

from logging import debug


class Input:
    session = None

    def __init__(self, test):
        self.stream = self.characters(test)
        self.queue = []
        
    def get(self):
        if self.queue:
            return self.queue.pop(0)
        c = next(self.stream)
        return c
    
    def put(self, c):
        self.queue.append(c)
        
    def characters(self, test):
        for s in test(self.session):
            while s:
                s0 = s
                if s[:2] == '^^':
                    yield '^'
                    s = s[2:]
                if s[0] == '^':
                    yield s[:2]
                    s = s[2:]
                elif s[:2] == '<<':
                    yield '<'
                    s = s[2:]
                elif s[0] == '<':
                    key, s = s[1:].split('>', 1)
                    yield key.replace('-', '_')
                elif s[0] == '\n':
                    s = s[1:]
                else:
                    yield s[0]
                    s = s[1:]
                debug(s0[:len(s0) - len(s)])
                

def test(names):
    if os.path.isdir('spelltinkle-self-test'):
        shutil.rmtree('spelltinkle-self-test')
    os.mkdir('spelltinkle-self-test')
    os.chdir('spelltinkle-self-test')
    prof = cProfile.Profile()
    prof.enable()
    if not names:
        names = all_tests
    for name in names:
        debug(name)
        t = getattr(tests, name)
        input = Input(t)
        run(getattr(t, 'args', []), input)
    prof.disable()
    prof.dump_stats('test.profile')

    
class Screen:
    def __init__(self, h=10, w=40):
        self.h = h
        self.w = w
        
    def subwin(self, a, b, c, d):
        return Screen(a, b)
        
    def erase(self):
        pass
        
    def refresh(self):
        pass
        
    def move(self, a, b):
        pass
        
    def write(self, line, colors):
        pass
    
    
if __name__ == '__main__':
    scr = Screen()
    for name in all_tests:
        print(name)
        t = getattr(tests, name)
        input = Input(t)
        filenames = getattr(t, 'args', [])
        s = Session(filenames, scr, input)
        try:
            s.run()
        except StopSession:
            pass
