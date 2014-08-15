"""
This file is part of snakewatch.

snakewatch is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

snakewatch is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with snakewatch.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import print_function, absolute_import, unicode_literals, division

import six

from abc import ABCMeta, abstractmethod, abstractproperty


@six.add_metaclass(ABCMeta)
class Input(object):
    """Base class for all Inputs"""

    pipe = None

    def connect_process(self, pipe):
        """Connect this input to the receiving end of a Pipe"""
        self.pipe = pipe
        
    def process_pipe(self):
        """Process any signals from the Pipe"""
        if self.pipe is not None:
            signal = None
            try:
                if self.pipe.poll():
                    signal = self.pipe.recv()
            except Exception:
                pass
            if signal == 'close':
                self.close()
    
    @abstractproperty
    def name(self):
        """Name of the Input"""
        return None
    
    @abstractmethod
    def open(self):
        """Open the Input and get ready for watching"""
        pass
    
    @abstractmethod
    def watch(self, started_callback, output_callback, int_callback):
        """Start watching the Input"""
        pass
    
    @abstractmethod
    def close(self):
        """Close the Input and any associated resources"""
        pass
