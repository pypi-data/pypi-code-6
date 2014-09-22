####################################################################################################
# 
# PyDvi - A Python Library to Process DVI Stream
# Copyright (C) 2014 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
####################################################################################################

####################################################################################################

from ..Widgets.ApplicationBase import ApplicationBase
from .MainWindow import MainWindow

####################################################################################################

class Application(ApplicationBase):

    ###############################################

    def __init__(self, args):

        super(Application, self).__init__(args)

        self._main_window = MainWindow()
        self._main_window.showMaximized()

####################################################################################################
# 
# End
# 
####################################################################################################
