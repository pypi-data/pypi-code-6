from spelltinkle.actions import Actions
from spelltinkle.document import Document


level0 = r"""\/OO
###################
        #
o       #
        #
#########

*

###################
Help: ...
###################
"""


class GameActions(Actions):
    def __init__(self, session):
        self.session = session

    def insert_character(self, doc, c):
        if c.isdigit():
            i = int(c)
            if 0 < i < len(self.session.docs):
                self.choose(i)
                
    def choose(self, i):
        self.session.docs.pop()
        self.session.docs.append(self.session.docs.pop(-i))
        self.session.docs[-1].view.set_screen(self.session.scr)
        self.session.docs[-1].changes = 42

    def enter(self, doc):
        self.choose(doc.view.r + 1)

    def esc(self, doc):
        self.choose(1)
                
    def view_files(self, doc):
        self.insert_character(doc, '2')
        
            
class Game(Document):
    def __init__(self, session):
        Document.__init__(self, actions=GameActions(session))
        self.name = '[game]'
        self.view.set_screen(session.scr)
        
        x, *y = level0.splitlines()
        n = max(len(line) for line in y)
        
        lines = [x] + ['#' + line.ljust(n) + '#' for line in y] + ['']
        self.change(0, 0, 0, 0, lines)
        