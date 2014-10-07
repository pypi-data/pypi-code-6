from .main import TuiElement

class LabelBox(TuiElement):
    """
    label box. contains text that is usually not changed by user.
    """
    
    def __init__ (self, **kwargs):
        """
        constructor. no special parameters needed.
        """
        
        super().__init__(**kwargs)
        
        #items is a 2d lists. each sublist contains characters for a single
        #line in the label box.
        self.items = []
        for c in range (kwargs['height']):
            self.items.append ([])
        
        #refresh screen
        self.draw()
    
    def clear (self):
        """
        sets text in the label box to empty string
        """
        
        self.settext('')
    
    def getline (self, n=-1):
        return ''.join (self.items[n]).strip ('\n')
    
    def _getline (self, n):
        
        #if visible return justified line
        #otherwise return erased line
        if self.isvisible:
            return self.get_justified_line (n)
        else:
            return self.geterased_line()
    
    def get_justified_line (self, row):
        """
        returns a justified line. spaces are added to the line string to make
        it justified properly.
        """
        
        if self.just == 'left':
            return ''.join (self.items[row][0:self.width]).replace('\n', '').ljust (self.width)
        elif self.just == 'right':
            return ''.join (self.items[row][0:self.width]).replace('\n', '').rjust (self.width)
        elif self.just == 'center':
            return ''.join (self.items[row][0:self.width]).replace('\n', '').center (self.width)
    
    def gettext(self):
        """
        returns all text in the label as a string object.
        """
        
        text = []
        for c in range (len(self.items)):
            text.append (''.join (self.items[c]))
        return ''.join (text)
    
    def settext(self, text):
        """
        erases all text in the label box and replaces it with another text.
        """
        
        #lock to block access from other threads
        with self.lock:
            #erase all text
            for c in range (len (self.items)):
                self.items[c] = []
            
            #cursor is used to check if reached the end of the box
            cursor = 0
            #row is the row we are writing at
            row = 0
            #loop counter
            c = 0
            
            #stop if row goes past box height or reached end of new text
            while row < self.height and c < len (text):
                #append 1 character and update cursor
                self.items[row].append (text[c])
                cursor += 1
                
                #increase row number if cursor goes past current line or
                #encountered a '\n'
                if cursor // self.width > row or text[c] == '\n':
                    row += 1
                    #updates cursor in case we got a '\n'
                    cursor = row * self.width
                c += 1
        
        #refresh screen
        self.draw()
