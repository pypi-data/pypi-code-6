import collections
import curses.ascii
import os
import queue
import traceback
from logging import debug
from time import time

from spelltinkle.actions import Actions
from spelltinkle.document import Document
from spelltinkle.exceptions import StopSession
from spelltinkle.keys import keynames, doubles, repeat, again


class Session:
    def __init__(self, filenames, scr, input):
        positions = self.read()
        if filenames:
            self.docs = []
            for filename in filenames:
                doc = Document(actions=Actions(self))
                doc.view.set_screen(scr)
                doc.read(filename, positions)
                self.docs.append(doc)
        else:
            self.docs = [Document(actions=Actions(self))]
            self.docs[0].view.set_screen(scr)

        self.scr = scr

        if input is None:
            self.queue = queue.Queue()
            scr.get_keys(self.queue)
        else:
            # This is a self-test:
            input.session = self
            self.queue = input
            
        self.lastkey = None
        self.lasttime = 0.0
        self.memory = ['']
        self.chars = ''
        self.lastsearchstring = ''

    @property
    def doc(self):
        return self.docs[-1]
        
    def run(self):
        while True:
            try:
                self.loop()
            except StopSession:
                raise
            #except:
            #    with open('st.tb', 'w') as fd:
            #        e = traceback.print_exc(file=fd)
            #    self.queue.put(['^o'] + list('st.tb') + ['enter'])

    def loop(self):
        for doc in self.docs[-1:]:
            for view in doc.views:
                view.update(self)
            if doc.changes:
                doc.color.run(self.queue)
            doc.changes = None

        doc = self.docs[-1]
        actions = doc.actions

        key = self.queue.get()
        if key == 'draw colors':
            doc.changes = 42
            doc.views[0].update(self)
            doc.changes = None
            return
        if isinstance(key, list):
            for k in key[1:]:
                self.queue.put(k)
            key = key[0]
        if len(key) == 1:
            self.chars += key
            actions.insert_character(doc, key)
        elif key == 'resize':
            self.scr.resize()
            for doc in self.docs:
                doc.changes = 42
        else:
            if key in doubles:
                key2 = self.queue.get()
                key = doubles[key].get(key2)
                if key is None:
                    return
            else:
                key = keynames.get(key, key)
                if key is None:
                    return
                if key[0] == '^':
                    return
            if isinstance(key, list):
                for k in key:
                    self.queue.put(k)
                return
            if key in again and key == self.lastkey:
                key += '_again'
            elif (key in repeat and key == self.lastkey and
                  time() < self.lasttime + 0.3):
                key += key
            method = getattr(actions, key, None)
            if method is None:
                if hasattr(actions, 'unknown'):
                    actions.unknown(doc, key)
            else:
                method(doc)
            if key.endswith('_again'):
                key = key[:-6]
        self.lastkey = key
        self.lasttime = time()
        if len(key) > 1:
            self.chars = ''

    def read(self):
        dct = collections.OrderedDict()
        path = os.path.expanduser('~/.spelltinkle/session.txt')
        if os.path.isfile(path):
            with open(path) as fd:
                for line in fd:
                    name, r, c = line.rsplit(maxsplit=2)
                    dct[name] = int(r), int(c)
        return dct

    def save(self):
        dct = self.read()
        for doc in self.docs:
            if doc.filename is not None:
                dct[os.path.abspath(doc.filename)] = doc.view.pos
        with open(os.path.expanduser('~/.spelltinkle/session.txt'), 'w') as fd:
            for name, (r, c) in dct.items():
                print(name, r, c, file=fd)
