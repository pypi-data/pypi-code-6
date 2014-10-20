import re
import threading
from logging import debug


TRANSLATION = bytes.maketrans(bytes(range(24)), bytes(list(range(12)) * 2))


def make_regular_expression(s):
    if s.islower():
        flags = re.IGNORECASE
    else:
        flags = 0
    return re.compile(re.escape(s), flags)
        
        
class Search:
    def __init__(self, session, doc, direction=1):
        self.session = session
        self.direction = direction
        
        self.string = None
        self.match = None
        self.positions = None
        self.paint_thread = None
        
        self.reset(doc)
        
    def reset(self, doc):
        self.string = ''
        self.match = ''
        self.update_info_line(doc.view)
        self.positions = [doc.view.pos + ('',)]

    def search_forward(self, doc, direction=1):
        if self.direction != direction:
            self.direction *= -1
            self.session.lastsearchstring = self.string
            self.reset(doc)
        if self.string == '':
            for c in self.session.lastsearchstring:
                self.string += c
                self.find(doc)
            self.paint(doc)
            return
        self.find(doc, True)

    def search_backward(self, doc):
        self.search_forward(doc, direction=-1)

    def insert_character(self, doc, c):
        self.string += c
        self.find(doc)
        self.paint(doc)
        
    def bs(self, doc):
        if len(self.string) > len(self.match):
            self.string = self.string[:-1]
            r, c = doc.view.pos
        elif len(self.positions) == 1:
            return
        else:
            self.positions.pop()
            r, c, self.string = self.positions[-1]
            self.match = self.string
        self.update_info_line(doc.view)
        doc.view.move(r, c)
        self.paint(doc)

    def unknown(self, doc, name):
        self.clean(doc)
        doc.view.message = None
        doc.view.update_info_line()
        self.session.lastsearchstring = self.string
        from .actions import Actions
        doc.actions = Actions(self.session)
        doc.view.update(self.session)
        getattr(doc.actions, name)(doc)
            
    def find(self, doc, next=False):
        d = self.direction
        reo = make_regular_expression(self.string[::d])
        r, c = doc.view.pos

        if d == 1:
            if next:
                c += len(self.match)

            for dr, line in enumerate(doc.lines[r:]):
                if dr == 0:
                    m = reo.search(line, c)
                else:
                    m = reo.search(line)
                if m:
                    c = m.start()
                    r += dr
                    self.match = self.string
                    self.update_info_line(doc.view)
                    self.positions.append((r, c, self.string))
                    doc.view.move(r, c)
                    return
        else:
            if next:
                c -= len(self.match)

            for dr, line in enumerate(doc.lines[r::-1]):
                N = len(line)
                if dr == 0:
                    m = reo.search(line[::-1], N - c)
                else:
                    m = reo.search(line[::-1])
                if m:
                    c = N - m.start() + 1
                    r -= dr
                    self.match = self.string
                    self.update_info_line(doc.view)
                    self.positions.append((r, c, self.string))
                    doc.view.move(r, c)
                    return
                    
        self.update_info_line(doc.view)
        doc.view.update(self.session)
                
    def update_info_line(self, view):
        view.message = 'Search: {}({})'.format(self.match,
                                               self.string[len(self.match):])
        view.update_info_line()

    def paint(self, doc):
        if self.paint_thread:
            self.paint_thread.join()
        self.paint_thread = threading.Thread(target=self.painter, args=[doc])
        self.paint_thread.start()
        
    def painter(self, doc):
        self.clean(doc)
        reo = make_regular_expression(self.string)
        for r, line in enumerate(doc.lines):
            for match in reo.finditer(line):
                for c in range(match.start(), match.end()):
                    doc.color.colors[r][c] += 12
        self.session.queue.put('draw colors')
                    
    def clean(self, doc):
        for line in doc.color.colors:
            line[:] = line.translate(TRANSLATION)
        