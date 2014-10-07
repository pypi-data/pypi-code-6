import re
from .main import manager
from .labelbox import LabelBox

class TextBox (LabelBox):
    """
    same as label box but has functions to change text. it handles keyboard
    input to write or erase text.
    """
    
    def __init__ (self, **kwargs):
        """
        constructor. no special arguments needed. it defines cursor position
        which indicates where the next character will be written relative to
        the element position. it also adds default handlers for '\\n',
        'BACKSPACE' and 'ALL'. these handlers can be overridden by the
        handlers parameter.
        by default, '\\n' event appends a new line to the text in the box.
        'BACKSPACE' event removes last character.
        'ALL'event accepts a character and appends it to the box.
        """
        
        #default handlers
        DEFAULT_HANDLERS = {'\n': (self.append_newline, {}),
                            'BACKSPACE': (self.pop_char, {}),
                            'ALL': (self.append_char, {}, 'event'),
                            }
        self.cursor = 0
        
        super().__init__(**kwargs)
        
        #if a default handler is not overridden, set it
        for c in DEFAULT_HANDLERS:
            if not c in self.handlers:
                self.handlers[c] = DEFAULT_HANDLERS[c]
        
        #refresh screen
        self.draw()
    
    def getcursor(self):
        """
        returns position of next character to be written.
        """
        
        #if visible calculate the cursor position
        if self.isvisible:
            #get y position. if box is full, return height - 1
            y = min (self.cursor // self.width, self.height-1)
            
            #get last line
            line = self.getline(y)
            #check how many spaces in the beginning of line
            #to be used later
            r = re.compile (' *$')
            match = r.search (line)
            if match:
                spaces = match.span()
                spaces = spaces[1] - spaces[0]
            else:
                spaces = 0
            
            #x position is length of justified line after removal
            #justification spaces at end.
            x = min (len (self.get_justified_line (y).rstrip() + ' '*spaces), self.width-1)
            
            #x position is zero? then correct for center or right justification
            if not x and self.just == 'center':
                #x position in middle
                x = (self.width-1) // 2
            elif not x and self.just == 'right':
                #x position at end
                x = self.width - 1
            
            return y, x
        else:
            #if not visible, return super() cursor
            return super().getcursor()
    
    def pop_char (self):
        """
        removes 1 character from the text box
        """
        
        #get current column and row position
        col = self.cursor % self.width
        row = self.cursor // self.width
        
        #if no characters in box, do nothing.
        if self.cursor == 0:
            return
        
        #if at beginning of row, remove last character, go to previous
        #line and update cursor
        elif col == 0:
            row -= 1
            self.items[row].pop()
            self.cursor = row * self.width + len (self.items[row])
            
            #refresh screen
            self.draw()
        
        #otherwise, remove last character and update cursor.
        else:
            self.items[row].pop()
            self.cursor -= 1
            
            #refresh screen
            self.draw()
    
    def append_char (self, char):
        """
        adds one character to the end of the text box
        """
        
        #if at end of line, do nothing
        if self.cursor >= self.width * self.height:
            return
        
        #else if char is one printable character, append it to end and update
        #cursor
        elif len(char) == 1 and char.isprintable():
            row = self.cursor // self.width
            self.items[row].append (char)
            
            self.cursor += 1
            
            #refresh screen
            self.draw()
    
    def append_newline (self):
        """
        appends a '\\n' to the text box. updates cursor accordingly.
        if on the last row, no character is appended and cursor is not
        updated.
        """
        
        char = '\n'
        row = self.cursor // self.width
        newrow = row + 1
        if newrow < self.height:
            self.items[row].append (char)
            self.cursor = newrow * self.width
            
            #refresh cursor
            manager.draw_put ('')
    
    def append_line (self, text):
        """
        appends lines to the end of the box. it appends '\\n' to any empty line.
        it removes a number lines from the beginning of the box equal to the
        number of lines in the text parameter.
        """
        
        #lock to block access from other threads
        with self.lock:
            #if multiple lines, split them.
            text = text.split ('\n')
            
            #divide lines that cannot fit in a single row into multiple lines
            c = 0
            while c < len (text):
                if len (text[c]) > self.width:
                    text.insert (c+1, text[c][self.width:])
                    text[c] = text[c][0:self.width]
                c += 1
            
            len1 = len (text)
            len2 = len (self.items)
            
            #move last lines to the beginning
            for c in range (len1, len2):
                self.items[c - len1] = self.items[c]
            
            #put new text at the end
            len1 = len (text[-len (self.items):])
            for c in range (0, len1):
                self.items[-len1 + c] = list (text[c])
            
            #append '\n' to old lines in the box that do not end in a '\n'
            for c in range (0, len2-1):
                if not self.items[c] or (len (self.items[c]) < self.width - 1 and
                        self.items[c][-1] != '\n'):
                    self.items[c].append ('\n')
        
        #update cursor position
        self.cursor = (self.height-1) * self.width + len (self.items[-1])
        
        #refresh screen
        self.draw()
    
    def settext (self, text):
        """
        removes text in the box and replaces it with the text parameter
        """
        
        #lock to block access from other threads
        with self.lock:
            #same settext as label box
            super().settext (text)
            #get new number of rows
            row = len(self.items) - 1
            while row > 0 and not self.items[row]:
                row -= 1
            #update cursor
            self.cursor = row * self.width + len (self.items[row])
