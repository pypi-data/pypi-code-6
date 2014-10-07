import sys
import re
import threading
import queue
from .getkey import getkey
import colorama

FORECOLOR_RE = re.compile (r'^\033\[3[0-7];(1|2|22)m$')
BACKCOLOR_RE = re.compile (r'^\033\[4[0-7]m$')

class TuiElement:
    """
    base user interface element. any user interface element should
    inherit this class.
    """
    def __init__ (self, x, y, height=1, width=79, fore='\033[30m',
            back='\033[40m', just='left', handlers = {}, isvisible=True, focus=True):
        """
        constructor of any subclass of TuiElement should call this
        constructor.
        x and y are 0 indexed x and y coordinates on the terminal window
        starting from the top left corner
        
        height and width are height and width of the element in number of
        characters
        
        fore and back are ansi foreground and background colors
        just is justification. it should be the string 'left', 'right' or
        'center'
        
        handlers is a dictionary. the keys are any strings describing events.
        some examples for key values are:
            -usually values that getkey() returns like 'a', 'b' and 'c'.
            the library sends any character pressed as it continuesly monitors
            keyboard inputs. other values are 'UP' and 'F4' for special keys.
            -'FOCUS' which is sent just before this element gets focus.
            -'UNFOCUS' which is sent just before this element goes out of
             focus
            -'ALL' which handles all events which do not have a specific
             handler
            -any other string can be used but the library nevers sends this
             event. it still can be sent by other functions.
        the values in the dictionary must be a sequence object. with the
        following:
            -the first element must be a callable to handle the event.
            -the second element in the sequence must be a dictionary
             containing keyword arguments to the event handler.
            -if string 'obj' is present in the sequence, the object recieving
             the event is given as the first parameter to the handler.
            -if the string 'event' is given, the event string is given as the
             second parameter to the handler.
        
        isvisible is a boolean used to indicate whether the object is visible
        or not. if False, the object will not be drawn even if its
        draw() is called. this parameter is not tested enough so far.
        
        focus is a boolean to indicate whether this element can get focus or
        not. if True, the object is added to the focus list and may get focus
        if '\\t' is pressed.
        """
        error = []
        
        #check for errors
        if type (x) != int or x < 0:
            error.append ('"x" must be int')
        if type (y) != int or y < 0:
            error.append ('"y" must be int')
        if type (height) != int or height <= 0:
            error.append ('"height" must be int greater than 0')
        if type (width) != int or width <= 0:
            error.append ('"width" must be int greater than 0')
        #fore must be a valid ansi foreground color code
        #back must be a valid ansi background color code
        if not FORECOLOR_RE.match(fore):
            error.append ('"fore" must be str with valid ansi foreground '
                          'color code: \\033[3x;ym, replace x with a number '
                          'between 0 and 7 and replace y with 1, 2 or 22')
        if not BACKCOLOR_RE.match(back):
            error.append ('"back" must be str with valid ansi background '
                          'color code: \\033[4xm, replace x with a number '
                          'between 0 and 7')
        if just not in ['left', 'right', 'center']:
            error.append ('"just" must be "left", "right" or "center"')
        for c in handlers:
            if not hasattr (handlers[c][0], '__call__') and type (handlers[c][1] == dict):
                error.append ('"handlers" must be a dictionary with values '
                'that are all functions')
                break
        
        #error present? stop pytui and raise error
        if error:
            stop()
            raise ValueError ('\n'.join (error))
        
        #no errors? initialize all members
        #if visible, also draw the object on terminal
        else:
            self.x = x
            self.y = y
            self.height = height
            self.width = width
            self.back = back
            self.fore = fore
            self.just = just
            self.handlers = handlers
            self.isvisible = isvisible
            manager.register (self, focus=focus)
            if self.isvisible:
                manager.draw_put (self)
            
            #lock is used to be thread safe in case some functions of
            #a subclasse change internal variables
            self.lock = threading.RLock()
    
    def getcursor(self):
        """
        gives the cursor position relative to the element position. it should
        return a tuple with two integers indicated the desired position the
        cursor should appear at.
        """
        
        #basic implimentation. set cursor to the bottom right corner of the
        #object
        return self.height-1, self.width-1
    
    def handle (self, event):
        """
        handles events. event should be a one of self.handlers keys. the first
        element in the corrisponding value in self.handlers is the handler
        of the event and it will be called. the second element in the value
        will be used as keyword arguments. if obj is present in the value,
        this object will be used as first parameter to the handler. if 'event'
        is present in the value, the event parameter of this function will be
        used as second parameter to the handler if 'obj' is present.
        otherwise, the event will be the first argument.
        """
        
        #arguments. contains this object and the event if necessary
        args = []
        
        #event is empty? return False. did not handle anything
        if not event:
            return False
        #event in handlers? handle it then return True.
        elif event in self.handlers:
            if 'obj' in self.handlers[event]:
                args.append (self)
            if 'event' in self.handlers[event]:
                args.append (event)
            self.handlers[event][0] (*args, **self.handlers[event][1])
            return True
        #event not in handlers but we have 'ALL' handler? handle event then
        #return True
        elif 'ALL' in self.handlers:
            if 'obj' in self.handlers['ALL']:
                args.append (self)
            if 'event' in self.handlers['ALL']:
                args.append (event)
            self.handlers['ALL'][0] (*args, **self.handlers['ALL'][1])
            return True
        #cannot handle? return False
        else:
            return False
    
    def getline (self, n):
        """
        returns unformatted line. n is the line number. should be overridden
        """
        
        #basic implementation. returns nothing.
        return ''
    
    def _getline (self, n):
        """
        returns formatted line for display on terminal. n is the line number.
        this function is called for all lines when this object is being drawn.
        should be overridden.
        """
        
        #basic implementation. returns spaces if visible or getrased_lines()
        #if invisible.
        if self.isvisible:
            return ''.ljust (self.width)
        else:
            return self.geterased_line ()
    
    def geterased_line (self):
        """
        returns spaces with terminal background colors to erase element.
        """
        return '\033[49m' + ''.ljust (self.width)
    
    def setvisible (self, visible=None):
        """
        makes the element visible or invisible. if visible is
        omitted, toggle visible state. otherwise, set it equal to visible
        parameter.
        """
        
        #visible is None? toggle self.isvisible
        if visible == None:
            self.isvisible = not self.isvisible
        #else set self.isvisible
        else:
            self.isvisible = visible
        #draw the element if visible or erase it if invisible
        manager.draw_put(self)
    
    def draw (self):
        """
        draw function. queus element to be drawn if visible.
        """
        
        if self.isvisible:
            manager.draw_put (self)
    
    def setcolor (self, fore=None, back=None):
        """
        sets foreground color and background color of the element. if fore
        or back is omitted, it will not be changed.
        """
        
        if fore:
            self.fore = fore
        if back:
            self.back = back
        
        #refresh screen
        self.draw()

class Manager:
    """
    object to manage screen and keyboard input. it manages drawing to the
    screen and forwarding keyboard inputs to interface elements. it also
    generates 'FOCUS' and 'UNFOCUS' events.
    an instance of this class is created once the module is imported. no 
    other instance is needed nor expected to be there.
    """
    
    def __init__ (self, handlers = None):
        """
        constructor. it sets internal variables and default handlers. if
        handlers is not omitted, default handlers are set.
        handlers parameter have to be a dictionary. the keys are events to
        handle. the values should be a sequence of size 2. the first element
        is a callable to handle the event. the second element is a dictionary
        with keyword arguments to callable. if the string 'event' is in the
        sequence, the event is given as the first parameter to the handler. if
        handlers parameter is omitte, the following default handlers are
        set.
        -'ESCAPE' to stop the pytui application
        -'\\t' to goes to next element in the focus list
        
        all functions in this class are for internal use and should not be
        called except for draw_put(). it is used append objects to the draw
        queue.
        """
        
        #interface elements defined in the program
        self.element_list = []
        #elements that may get focus
        self.focus_list = []
        #index of current focused element
        self.focused = None
        
        #if handlers parameter present, set handlers
        #otherwise, set default handlers
        if handlers != None:
            self.handlers = handlers
        else:
            self.handlers = {'\t': (self.setfocus, {}), 'ESCAPE': (self.stop, {})}
        
        self.draw_queue = queue.Queue()
        
        #if True, application is stopped after a few seconds
        self.isstopped = False
        
        #draw_thread monitors draw events
        #input_thread monitors keyboard events
        self.draw_thread = threading.Thread (target = self.draw)
        self.input_thread = threading.Thread (target = self.handle)
    
    def start (self):
        """
        start pytui application and blocks until self.stop() is called.
        """
        
        self.start_nojoin()
        self.join()
    
    def start_nojoin(self):
        """
        starts pytui application but does not block. thread calling this
        function continues to execute while the pytui application is running.
        """
        
        self.draw_thread.start()
        self.input_thread.start()
    
    def join (self):
        """
        blocks until the self.stop is called.
        """
        
        self.draw_thread.join()
        self.input_thread.join()
    
    def stop (self):
        """
        stop the pytui application. self.start() will return after a few
        seconds from calling this function.
        """
        
        self.isstopped = True
    
    def draw_put (self, obj):
        """
        append obj to the draw queue to be processed by the draw thread.
        """
        
        self.draw_queue.put (obj)
    
    def draw (self):
        """
        draw function. it monitors draw queue and draws any object it sees.
        finding empty string refreshes screen cursor.
        the function terminates if self.isstopped is True.
        """
        
        #object to be drawn. start with None
        obj = None
        while not self.isstopped:
            #if there is object to draw, draw it
            while obj:
                try:
                    #do actual drawing
                    self._draw (obj)
                    #get new object to draw
                    obj = self.draw_queue.get(timeout=0.01)
                
                #no object, then set obj to empty string to refresh cursor
                except queue.Empty:
                    obj = ''
                #unexpected exception? stop and raise
                except Exception:
                    stop()
                    raise
            
            #if obj is empty string, refresh screen cursor
            if obj == '':
                #reset obj so you do not refresh cursor everytime
                obj = None
                self.update_cursor()
            
            try:
                #get another object to draw
                obj = self.draw_queue.get(timeout=0.01)
            #if no object, do nothing. even do not refresh cursor since
            #no object was drawn yet
            except queue.Empty:
                pass
            #unexpected exception? stop and raise
            except Exception:
                stop()
                raise
    
    def _draw (self, obj):
        """
        this function does actual drawing. obj is the object to draw.
        """
        
        #get x and y positions of the object
        x, y = obj.x, obj.y
        #set colors to object colors
        self.setcolor (obj.fore, obj.back)
        
        #get all lines and print them
        for c in range (obj.height):
            #set terminal cursor to beginning of line inside the object
            self._setcursor_no_flush (y+c, x)
            print (obj._getline(c), end='')
    
    def handle (self):
        """
        handles events. if event is in self.handlers keys, it is called.
        otherwise, the event is sent to the element on focus. the first
        element in the corrisponding value in self.handlers is the handler
        of the event and it will be called. the second element in the value
        will be used as keyword arguments. if 'event' is present in the value,
        the event parameter of this function will be used as first parameter.
        """
        
        #loop until stopped
        while not self.isstopped:
            #get keyboard press with 2 deciseconds timeout
            char = getkey(2)
            
            #non-keyword arguments
            args = []
            #if handler present in manager, handle event
            if char in self.handlers:
                #add char as parameter if 'event' is present in the sequence
                if 'event' in self.handlers[char]:
                    args.append (char)
                self.handlers[char][0] (*args, **self.handlers[char][1])
            #else if 'ALL' is present, use it to handle all other events
            elif 'ALL' in self.handlers:
                #add char as parameter if 'event' is present in the sequence
                if 'event' in self.handlers['ALL']:
                    args.append (char)
                self.handlers['ALL'][0] (*args, **self.handlers['ALL'][1])
            #no handler? then send to focused object
            elif self.focus_list:
                self.focus_list[self.focused].handle (char)
    
    def add_focus (self, obj):
        """
        add object to focus list.
        """
        
        #add only if object is not in list
        if not obj in self.focus_list:
            self.focus_list.append (obj)
        #if this is the first element, set self.focused to 0
        #also send 'FOCUS' event
        if self.focused == None:
            self.focused = 0
            self.focus_list[self.focused].handle ('FOCUS')
            #refresh screen cursor
            self.draw_queue.put ('')
    
    def del_focus (self, obj):
        """
        delete object from focus list.
        """
        
        try:
            self.focus_list.remove (obj)
            #if focus list is empty, set self.focused to None
            if not self.focus_list:
                self.focused = None
            #if focus list is not empty and last element is removed, focus
            #on the previous element
            elif self.focused > len (self.focus_list):
                self.focused -= 1
        #object is not present? do nothing
        except ValueError:
            pass
        #unexpected exception? stop and raise
        except Exception:
            stop()
            raise
        
    def setfocus (self, n=None):
        """
        set on focus object. n can be the index of the object in the focus
        list or the object itself. if n is omitted, focus on the next element
        on the list. if reached last element, focus on the first element. this
        function sends 'UNFOCUS' event to the object on focus and sends
        'FOCUS' event to the element to be on focus.
        """
        
        #if n is None, choose the next element
        if n == None:
            n = (self.focused + 1) % len (self.focus_list)
        #if n is a TuiElement, find its index in the focus_list
        elif isinstance(n, TuiElement):
            n = self.focus_list.index (n)
        
        
        #send 'UNFOCUS'
        self.focus_list[self.focused].handle ('UNFOCUS')
        #change focus index
        self.focused = n
        #send 'FOCUS'
        self.focus_list[self.focused].handle ('FOCUS')
        #refresh screen cursor
        self.draw_queue.put ('')
    
    def _setcursor_no_flush (self, y, x):
        """
        sets cursor position but does not flush stdout.
        """
        
        print ('\x1b['+str(y+1)+';'+str(x+1)+'H', end='')
    
    def setcursor (self, y, x):
        """
        sets cursor position.
        """
        
        self._setcursor_no_flush (y, x)
        sys.stdout.flush()
    
    def getcursor (self):
        """
        returns cursor position of the the element on focus relative to the
        terminal screen.
        """
        
        #get object
        obj = self.focus_list[self.focused]
        #get cursor relative to object
        cursor = list (obj.getcursor())
        #convert to cursor relative to screen
        cursor[0] += obj.y
        cursor[1] += obj.x
        
        return cursor
    
    def setcolor (self, fore=None, back=None):
        """
        sets fore and background color of the terminal. if any parameter is
        omitted, it will not be changed.
        """
        
        color = ''
        if fore:
            color += fore
        if back:
            color += back
        
        print (color, end='')
    
    def update_cursor (self):
        """
        resets cursor to the position of the focused object.
        """
        obj = self.focus_list[self.focused]
        cursor = list (obj.getcursor())
        cursor[0] += obj.y
        cursor[1] += obj.x
        self.setcursor (*cursor)
    
    def register (self, obj, focus=True):
        """
        register object to the manager element list. if focus is True, the
        object is also added to the focus list.
        """
        
        #add only if not in element list
        if obj not in self.element_list:
            self.element_list.append (obj)
        #add only if not in focus list
        if obj not in self.focus_list and focus:
            self.add_focus (obj)
    
    def unregister (self, obj):
        """
        remove object from element and focus lists.
        """
        
        #remove from focus list
        try:
            self.focus_list.remove (obj)
            #remove if in focus list.
            if not self.focus_list:
                self.focused = None
            #if last element is removed, focus on last element
            elif self.focused > len (self.focus_list):
                self.focused -= 1
        #if element is not in list, ignore
        except ValueError:
            pass
        #unexpected exception? stop and raise
        except Exception:
            stop()
            raise
        
        #remove from element list
        try:
            self.element_list.remove (obj)
        #if element is not in list, ignore
        except ValueError:
            pass
        #unexpected exception? stop and raise
        except Exception:
            stop()
            raise
        


def start():
    """
    start pytui application. initialize colorama and start the application.
    blocks until application ends.
    """
    
    colorama.init()
    manager.start()
    
def stop ():
    """
    deinitialize colorama and stops application.
    """
    
    colorama.deinit()
    manager.stop()

def ignore_event ():
    """
    function that does nothing. it can be used as a handler to ignore events.
    """
    
    pass

#manager to manage interface elements.
manager = Manager()

