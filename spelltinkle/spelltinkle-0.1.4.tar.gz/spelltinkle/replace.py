import re
import threading
from logging import debug

from spelltinkle.input import InputActions

        
class Replace(InputActions):
    def __init__(self, session, doc):
        InputActions.__init__(self, session)

        self.find = None
        self.regex = None
        self.replace = None
        self.paint_thread = None
        self.update(doc, '')
        
    def update(self, doc, string=None):
        InputActions.update(self, doc, string)
        if self.find is None:
            text = 'Find:' + string
        elif self.replace is None:
            text = 'Replace:' + string
        else:
            text = 'Replace?  yes, no or all!'
        doc.view.message = text
        doc.view.update_info_line()
        
    def enter(self, doc):
        if self.find is None:
            self.find = self.string
            self.regex = re.compile(re.escape(self.find))
            self.c = 0
            self.update(doc, '')
            return
        
        if self.replace is None:
            self.replace = self.string
            self.next(doc)
            self.update(doc)
            
    def insert_character(self, doc, chr):
        if self.replace is None:
            InputActions.insert_character(self, doc, chr)
            return
            
        r, c = doc.view.pos
        
        if chr == 'n':
            doc.view.move(r, c + len(self.find))
            self.next(doc)
        elif chr == 'y':
            doc.change(r, c, r, c + len(self.find), [self.replace])
            self.next(doc)
        elif chr == '!':
            while True:
                doc.change(r, c, r, c + len(self.find), [self.replace])
                if not self.next(doc):
                    break
                r, c = doc.view.moved
                
    def next(self, doc):
        if doc.view.moved:
            r, c = doc.view.moved
        else:
            r, c = doc.view.pos
        for r, c, line in doc.enumerate(r, c):
            match = self.regex.search(line)
            if match:
                c += match.start()
                doc.view.move(r, c)
                return True

        self.esc(doc)
        return False
                
    def esc(self, doc):
        #self.clean(doc)
        doc.view.message = None
        doc.view.update_info_line()
        from .actions import Actions
        doc.actions = Actions(self.session)
        doc.view.update(self.session)
        
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
        