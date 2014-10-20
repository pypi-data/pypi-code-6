class InputActions:
    def __init__(self, session):
        self.session = session
        self.c = 0
        self.string = ''

    def update(self, doc, string=None):
        if string is not None:
            self.string = string
        
    def insert_character(self, doc, chr):
        s = self.string[:self.c] + chr + self.string[self.c:]
        self.c += 1
        self.update(doc, s)
        
    def bs(self, doc):
        s = self.string[:self.c - 1] + self.string[self.c:]
        self.c -= 1
        self.update(doc, s)
        
    def delete(self, doc):
        s = self.string[:self.c] + self.string[self.c + 1:]
        self.update(doc, s)
        
    def left(self, doc):
        self.c = max(0, self.c - 1)
        self.update(doc)

    def right(self, doc):
        self.c = min(len(self.string), self.c + 1)
        self.update(doc)

    def home(self, doc):
        self.c = 0
        self.update(doc)

    def end(self, doc):
        self.c = len(self.string)
        self.update(doc)
