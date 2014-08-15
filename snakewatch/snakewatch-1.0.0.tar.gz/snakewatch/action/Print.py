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

import re

from colorama import Fore, Back, Style

from ._Action import Action


class PrintAction(Action):
    """An Action that returns the line with possible colouring"""

    non_char = re.compile('[^a-zA-Z]+')
    styleable = ['fore', 'back', 'style']
    
    def __init__(self, cfg):
        super(PrintAction, self).__init__(cfg)
        for part in self.styleable:
            if part in self.cfg:
                self.cfg[part] = self.non_char.sub('', self.cfg[part]).upper()
                
        style = Style.RESET_ALL
        if 'fore' in self.cfg and hasattr(Fore, self.cfg['fore']):
            style = ''.join([style, getattr(Fore, self.cfg['fore'])])
        if 'back' in self.cfg and hasattr(Back, self.cfg['back']):
            style = ''.join([style, getattr(Back, self.cfg['back'])])
        if 'style' in self.cfg and hasattr(Style, self.cfg['style']):
            style = ''.join([style, getattr(Style, self.cfg['style'])])
            
        self.style = style
        
    def run_on(self, line):
        return ''.join([self.style, line])

    def release_resources(self):
        pass
