# coding: utf-8

""" Module provides tools for shifting output from scopes wrapped with the 'with' statement.
    For example, this code:
        >>> from shift_print import shift
        >>> def test_print(depth, level=0):
        ...     ''' Test recursive printing
        ...     '''
        ...     if depth <= 0:
        ...         return
        ...     print "LEVEL:", level
        ...     with shift():
        ...         test_print(depth-1, level+1)
        ... 
        >>> test_print(5)

    Will produce this output:
        LEVEL: 0
            LEVEL: 1
                LEVEL: 2
                    LEVEL: 3
                        LEVEL: 4


    One more example:
        >>> import sys
        >>> from shift_print import shift_both
        >>>
        >>> def test_print(depth, level=0):
        ...     ''' Test recursive printing
        ...     '''
        ...     if depth <= 0:
        ...         return
        ...     print "OUT:", level
        ...     print >>sys.stderr, "ERR:", level
        ...     print
        ...     print >>sys.stderr
        ...     with shift_both():
        ...         test_print(depth-1, level+1)
        ...
        >>> with shift_both(out_space=' +  ', err_space='  + ', level=1):
        ...     test_print(5)
        ... 

    Output will be:
         +  OUT: 0
          + ERR: 0
         +  
          + 
         +   +  OUT: 1
          +   + ERR: 1
         +   +  
          +   + 
         +   +   +  OUT: 2
          +   +   + ERR: 2
         +   +   +  
          +   +   + 
         +   +   +   +  OUT: 3
          +   +   +   + ERR: 3
         +   +   +   +  
          +   +   +   + 
         +   +   +   +   +  OUT: 4
          +   +   +   +   + ERR: 4
         +   +   +   +   +  
          +   +   +   +   + 
"""


import sys
from StringIO import StringIO


def shift(*args, **kwargs):
    """ Helper function. Creates context for shifting sys.stdout if it does not exists,
        otherwise increases shift level.
        For example, this code:
            >>> from shift_print import shift
            >>> def test_print(depth, level=0):
            ...     ''' Test recursive printing
            ...     '''
            ...     if depth <= 0:
            ...         return
            ...     print "LEVEL:", level
            ...     with shift():
            ...         test_print(depth-1, level+1)
            ... 
            >>> test_print(5)

        Will produce this output:
            LEVEL: 0
                LEVEL: 1
                    LEVEL: 2
                        LEVEL: 3
                            LEVEL: 4    
    """
    if isinstance(ShiftContext.current(), ShiftPrintScope):
        return ShiftMore()
    else:
        kwargs['level'] = kwargs['level'] if 'level' in kwargs else 1
        return ShiftPrintScope(*args, **kwargs)


def shift_out(*args, **kwargs):
    """ Helper function. Creates context for shifting sys.stdout if it does not exists,
        otherwise increases shift level.
        See help(shift_print.shift) for an example.
    """
    if isinstance(ShiftContext.current(), ShiftPrintScope):
        return ShiftMore()
    else:
        kwargs['level'] = kwargs['level'] if 'level' in kwargs else 1
        return ShiftPrintScope(*args, stdout=True, **kwargs)


def shift_err(*args, **kwargs):
    """ Helper function. Creates context for shifting sys.stderr if it does not exists,
        otherwise increases shift level.
        See help(shift_print.shift) for an example.
    """
    if isinstance(ShiftContext.current(), ShiftPrintScope):
        return ShiftMore()
    else:
        kwargs['level'] = kwargs['level'] if 'level' in kwargs else 1
        return ShiftPrintScope(*args, stdout=False, stderr=True, **kwargs)


def shift_both(*args, **kwargs):
    """ Helper function. Creates context for shifting sys.stdout and sys.stderr if it does not exists,
        otherwise increases shift level.
        See help(shift_print.shift) for an example.
    """
    if isinstance(ShiftContext.current(), ShiftPrintScope):
        return ShiftMore()
    else:
        kwargs['level'] = kwargs['level'] if 'level' in kwargs else 1
        return ShiftPrintScope(*args, stdout=True, stderr=True, **kwargs)


def deep_print(depth, level=0):
    """ Test recursive printing
    """
    if depth <= 0:
        return
    print "OUT:", level
    print >>sys.stderr, "ERR:", level
    print
    print >>sys.stderr
    with ShiftMore():
        deep_print(depth-1, level+1)


def deep_write(file, depth, level=0):
    """ Test recursive writing
    """
    if depth <= 0:
        return
    file.write("WRITE: {}\n".format(level))
    file.write("\n")
    with ShiftMore():
        deep_write(file, depth-1, level+1)


class BasicShiftingStream(object):
    """ Basic class for shifting stream wrappers.
        Class defines minimal required interface that allows
        stream to be used with ShiftContext.
    """
    def __init__(self):
        self._level = 0

    def level(self):
        """ Get current level
        """
        return self._level

    def set_level(self, level):
        """ Explicitly set level value
        """
        self._level = level

    def inc_level(self):
        """ Increase shifting level by 1
        """
        self._level += 1

    def dec_level(self):
        """ Decrease shifting level by 1
        """
        self._level -= 1


class ShiftingStream(BasicShiftingStream):
    """ Wraps an object with a 'write' and 'writelines' attributes
        and writes an offset before writing the actial data.
    """
    def __init__(self, stream, space=u'    '):
        """ stream - a stream that will be wrapped. It must have 'write' method.
            space - a string that will be used to shift output per level.
        """
        super(ShiftingStream, self).__init__()
        self._stream = stream
        self.space = space
        self._level = 0
        self.new_line = True

    def _write_space(self):
        for i in xrange(self._level):
            self._stream.write(self.space)

    def _write(self, str):
        if self.new_line:
            self._write_space()
            self.new_line = False

        self._stream.write(str)

    def writelines(self, lines):
        lines = [lines] if isinstance(lines, basestring) else lines
        for line in lines:
            self.write(line)

    def write(self, str):
        if not str:
            return

        splitted = str.split('\n')
        last_is_new_line = (splitted[-1] == '')
        if last_is_new_line:
            splitted.pop()

        for line in splitted[:-1]:
            self._write(line)
            self._write('\n')
            self.new_line = True

        self._write(splitted[-1])

        if last_is_new_line:
            self._write('\n')
            self.new_line = True

    def __getattr__(self, name):
        return getattr(self._stream, name)


class ShiftContext(object):
    """ Defines a context for Shift subscopes.
    """
    _stack = []

    @classmethod
    def current(cls):
        if cls._stack:
            return cls._stack[-1]
        else:
            return None

    def _on_enter(self):
        #self.sub_stream(self.my_custom_stream):
        pass

    def _on_exit(self):
        pass

    def __init__(self):
        self._streams = []

    def __enter__(self):
        result = self._on_enter()
        ShiftContext._stack.append(self)
        return result

    def __exit__(self, exc_type, value, trace):
        ShiftContext._stack.pop()
        self._on_exit()
        self._streams = []

    def sub_stream(self, stream):
        self._streams.append(stream)

    def inc_level(self):
        for stream in self._streams:
            stream.inc_level()

    def dec_level(self):
        for stream in self._streams:
            stream.dec_level()        


class ShiftPrintScope(ShiftContext):
    """ Allows to shift all stdout and/or stderr output written from scopes wrapped with the 'with' statement.
        Usage example:
            >>> from shift_print import ShiftPrintScope, ShiftMore
            >>> with ShiftPrintScope():
            ...     print "A"
            ...     with ShiftMore():
            ...         print "B"
            ...         print "C"
            ...         with ShiftMore():
            ...             print "D"
            ...         print
            ...         print "E"
            ...     print "F"
            ... 
            A
                B
                C
                    D
                
                E
            F
    """
    def __init__(self, space='    ', stdout=True, stderr=False, out_space=None, err_space=None, level=0):
        """ space - a string that will be used to shift output per level.
            stdout, stderr - if True, sys.stdout will be replaced with shifting stream for the wrapped scope.
            out_space, err_space - using these arguments you can specify different spacings for stdout and stderr.
            level - initial shifting level.
        """
        super(ShiftPrintScope, self).__init__()
        self.grab_stdout = stdout
        self.grab_stderr = stderr

        self.space = space
        self.out_space = out_space or self.space
        self.err_space = err_space or self.space
        self.start_level = level

        self.previous_stdout = None
        self.previous_stderr = None

    def _grab_stdout(self):
        self.previous_stdout = sys.stdout
        self.stdout = ShiftingStream(sys.stdout, self.out_space)
        self.stdout.set_level(self.start_level)
        sys.stdout = self.stdout
        self.sub_stream(self.stdout)

    def _grab_stderr(self):
        self.previous_stderr = sys.stderr
        self.stderr = ShiftingStream(sys.stderr, self.err_space)
        self.stderr.set_level(self.start_level)
        sys.stderr = self.stderr
        self.sub_stream(self.stderr)

    def _on_enter(self):
        if self.grab_stdout:
            self._grab_stdout()

        if self.grab_stderr:
            self._grab_stderr()

    def _on_exit(self):
        if self.previous_stdout:
            sys.stdout = self.previous_stdout
            self.stdout = None
            self.previous_stdout = None

        if self.previous_stderr:
            sys.stderr = self.previous_stderr
            self.stderr = None
            self.previous_stderr = None


class ShiftStreamScope(ShiftContext):
    """ Allows to shift all stdout and/or stderr output written from scopes wrapped with the 'with' statement.
        Example, this code:
            >>> from shift_print import Shift, ShiftStreamScope
            >>> def test_write(file, depth, level=0):
            ...     ''' Test recursive writing
            ...     '''
            ...     if depth <= 0:
            ...         return
            ...     file.write("WRITE: {}\n".format(level))
            ...     file.write("\n")
            ...     with Shift():
            ...         test_write(file, depth-1, level+1)
            ... 
            >>> with open('output', 'w') as f:
            ...     with ShiftStreamScope(f) as f:
            ...         test_write(f, 5)

        Will create a file named 'output' with this content:
            WRITE: 0

                WRITE: 1
                
                    WRITE: 2
                    
                        WRITE: 3
                        
                            WRITE: 4
                            
    """
    def __init__(self, stream, space='    '):
        """ stream - a stream to be wrapped for a scope.
            space - a string that will be used to shift output per level.
        """
        super(ShiftStreamScope, self).__init__()
        self.space = space
        self.shifting_stream = stream if isinstance(stream, BasicShiftingStream) else ShiftingStream(stream, self.space)

    def wrapped(self):
        """ Returns shifting stream that is the original stream wrapped by ShiftingStream
            (If it was not already)
        """
        return self.shifting_stream

    def _on_enter(self):
        self.sub_stream(self.shifting_stream)
        return self.shifting_stream


class ShiftMore(object):
    """ Shift scope.
        Increases shifting for all streams of the current ShiftContext.
    """
    def __init__(self):
        self.shift_context = ShiftContext.current()

    def __enter__(self):
        if self.shift_context:
            self.shift_context.inc_level()

    def __exit__(self, exc_type, value, trace):
        if self.shift_context:
            self.shift_context.dec_level()


class StdTrap(object):
    """ Allows to capture all stdout and/or stderr from scopes wrapped with the 'with' statement.
        Usage example:
            >>> from shift_print import StdTrap
            >>> grabber = StdTrap()
            >>> with grabber:
            ...     print "Some output"
            ... 
            >>> grabber.stdout.getvalue()
            'Some output\n'
            >>>
    """
    def __init__(self, stdout=True, stderr=False):
        self.stdout = StringIO() if stdout is True else stdout
        self.stderr = StringIO() if stderr is True else stderr

    def __enter__(self):
        if self.stdout:
            self.previous_out = sys.stdout
            sys.stdout = self.stdout

        if self.stderr:
            self.previous_err = sys.stderr
            sys.stderr = self.stderr

    def __exit__(self, type, value, trace):
        if self.stdout:
            sys.stdout = self.previous_out

        if self.stderr:
            sys.stderr = self.previous_err
