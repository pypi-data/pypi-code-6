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

import sys

from ._Input import Input


class STDInput(Input):
    """Input handler for sys.stdin"""

    def __init__(self):
        self.closed = True
    
    def name(self):
        return 'stdin'
    
    def open(self):
        self.closed = False
    
    def watch(self, started_callback, output_callback, int_callback):
        self.open()
        started_callback()
        
        while not self.closed:
            try:
                line = sys.stdin.readline()
                if line != '':
                    output_callback(line)
            except:
                pass
            
            self.process_pipe()
    
    def close(self):
        self.closed = True
