from .main import TuiElement, FORECOLOR_RE, BACKCOLOR_RE

class ListBox(TuiElement):
    """
    list of items. this class manages scrolling if the number of items it has
    is more then its height.
    """
    
    def __init__ (self, selected_fore=None, selected_back=None, **kwargs):
        """
        constructor. new arguments are selected_fore and selected_back. they
        set the foreground and background colors of the selected item in the
        list. it also adds default handlers for 'UP' and 'DOWN'. these
        handlers can be overridden by the handlers parameter.
        by default, 'UP' event goes to the previous item.
        'DOWN' event goes to the next item.
        """
        
        DEFAULT_HANDLERS = {'UP': (self.decselected, {}),
                            'DOWN': (self.incselected, {}),
                            }
        
        error = []
        #call super().__init__() and check for errors
        try:
            super().__init__(**kwargs)
        except ValueError as err:
            error.append (str (err))
        except Exception:
            stop()
            raise
        
        #check if selected_fore and selected_back are valid
        if selected_fore != None and not FORECOLOR_RE.match(selected_fore):
            error.append ('"selected_fore" must be None or str with valid '
                          'ansi foreground color code: \\033[3x;ym, replace '
                          'x with a number between 0 and 7 and replace y '
                          'with 1, 2 or 22')
        if selected_back != None and not BACKCOLOR_RE.match(selected_back):
            error.append ('"selected_back" must be None or str with valid '
                          'ansi background color code: \\033[4xm, replace x '
                          'with a number between 0 and 7')
        
        #raise errors if present
        if error:
            stop()
            raise ValueError ('\n'.join (error))
        
        #if default handlers are not overridden, add them to handlers
        for c in DEFAULT_HANDLERS:
            if not c in self.handlers:
                self.handlers[c] = DEFAULT_HANDLERS[c]
        
        #items in the list
        self.items = []
        
        #if selected_fore is None, make it the same as background color with
        #no bright or dim property
        #if selected_back is None, make it the same as foreground color
        if selected_fore == None:
            selected_fore = kwargs['back'].replace ('[4', '[3').replace ('m', ';22m')
        if selected_back == None:
            selected_back = kwargs['fore'].replace (';1', '').replace(';22', '')
            selected_back = selected_back.replace ('[3', '[4')
        
        self.selected_fore = selected_fore
        self.selected_back = selected_back
        
        #selected element index
        self.selected = 0
        #index of the element displayed at the top of the list
        self.top = 0
        
        #refresh screen
        self.draw()
    
    def setcolor (self, fore=None, back=None,
                    selected_fore=None, selected_back=None):
        """
        sets foreground color, background color, selected item foreground
        color and selected item background color. all parameters are optional
        and are ignored if not given.
        """
        if fore:
            self.fore = fore
        if back:
            self.back = back
        if selected_fore:
            self.selected_fore = selected_fore
        if selected_back:
            self.selected_back = selected_back
        
        #refresh screen
        self.draw()
            
    
    def getcursor (self):
        """
        returns the position of the most right cell in the selected item row.
        """
        
        #if visible return most right cell of selected item
        #otherwise, return super.getcursor()s
        if self.isvisible:
            return self.selected - self.top, self.width-1
        else:
            return super().getcursor()
    
    def clear (self):
        """
        remove all items in the list.
        """
        
        self.items = []
        #refresh screen
        self.draw()
    
    def _getline (self, n):
        
        #if visible return justified line
        #otherwise return erased line
        if self.isvisible:
            return self.get_justified_line (n)
        else:
            return self.geterased_line (n)
    
    def get_justified_line (self, n):
        """
        returns the string of the item to be drawn in line n. if the list is
        scrolled down, then the index of the item is not n but more than n.
        """
        
        #if item is within the height of the list, return it
        #else return nothing
        if n + self.top < len (self.items):
            text = str (self.items[n + self.top])
        else:
            text = ''
        
        #justify the text.
        if self.just == 'left':
            text = text.replace('\n', '').ljust (self.width)[0:self.width]
        elif self.just == 'right':
            text = text.replace('\n', '').rjust (self.width)[0:self.width]
        elif self.just == 'center':
            text = text.replace('\n', '').center (self.width)[0:self.width]
        
        #if the item is the selected one, return its fore and background
        #colors along with the text then reset to normal fore and background
        #otherwise, just return the text
        if n + self.top == self.selected:
            return (self.selected_fore + self.selected_back + text +
                         self.fore + self.back)
        else:
            return text
    
    def gettext(self):
        """
        return all the items as a string seperated by '\\n'
        """
        
        return '\n'.join (self.items)
    
    def insert(self, item, index=None):
        """
        insert a new element to the list at index. if index is omitted, insert
        at end of list.
        """
        
        #lock to block access from other threads
        with self.lock:
            #if index is None, append at end
            if index == None: index = len(self.items)
            #if there are items, fix the selected index to keep the same item
            #selected after insertion
            #also fix the self.top to keep the selected item visible in the
            #screen
            if self.items:
                if index <= self.selected:
                    self.selected += 1
                if self.selected >= self.top + self.height:
                    self.top += 1
            #insert item
            self.items.insert (index, item)
            #refresh screen
            self.draw()
    
    def pop(self, index=None):
        """
        remove an element from the list at index. if index is omitted, remove
        the last element.
        """
        
        #lock to block access from other threads
        with self.lock:
            #if index is None, remove last
            if index == None: index = len (self.items)-1
            
            #fix selected item so the same item is selected after removal
            if index < self.selected:
                self.selected -= 1
            
            #make sure the selected index is within the new list length
            if self.selected >= len (self.items) - 1:
                self.selected = len (self.items) - 2
            
            #if the selected index is negative, make it 0
            if self.selected < 0:
                self.selected = 0
            
            #fix self.top so the selected item is visible in the screen after
            #removal
            if self.selected < self.top:
                self.top -= 1
            #remove item
            self.items.pop (index)
            #refresh screen
            self.draw()
                    
    
    def getselected (self):
        """
        return selected item or None if index is out of range.
        """
        
        try:
            return self.items[self.selected]
        except IndexError:
            return None
    
    def decselected (self):
        """
        decrease selected index.
        """
        
        #make sure selected is positive
        self.selected = max (0, self.selected - 1)
        #if selected is above the visible list, make it at the top of visible
        #list
        if self.selected < self.top:
            self.top = self.selected
        
        #refresh screen
        self.draw()
    
    def incselected (self):
        """
        increase selected index.
        """
        
        #if there are items on the list, set selected index
        #otherwise do nothing
        if len(self.items) > 0:
            #make sure list length is not exceeded
            self.selected = min (len (self.items) - 1, self.selected + 1)
            #if selected is below the visible list, set top so that the
            #selected item is at the bottom of the list
            if self.selected >= self.top + self.height:
                self.top = self.selected - self.height + 1
            
            #refresh screen
            self.draw()
    
    def setselected (self, index):
        """
        set selected index to the index parameter value.
        """
        
        #if no items ignore
        if not self.items:
            return
        
        #if index is negative set selected index to 0
        if index < 0:
            self.selected = 0
        
        #if index is out of valid range, set selected to last element
        elif index >= len (self.items):
            self.selected = len(self.items) - 1
        
        #index is valid, set selected to index
        else:
            self.selected = index
        
        #if selected item is above visible items, make it the top visible
        if self.selected < self.top:
            self.top = self.selected
        
        #if selected item is below visible items, make it the bottom visible
        elif self.selected >= self.top + self.height:
            self.top = self.selected - self.height + 1
        
        #refresh screen
        self.draw()
    
    def clear (self):
        """
        empty the list.
        """
        
        self.selected = 0
        self.items = []

