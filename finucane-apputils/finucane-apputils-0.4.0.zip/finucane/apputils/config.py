# -*- coding: utf-8 -*-
"""finucane.apputils.config

Provides customized application configuration facilities and utilities. If a
customized or enhanced application configuration ability is needed, this is
where it should exist.

:copyright: (c) 2014 by Sean Anthony Finucane.
:license: MIT, see LICENSE for more details.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
# Python 2.6 and newer support
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from finucane.apputils.compatibility import upgrade_namespace
upgrade_namespace(globals())

try:
    import configparser  # Python 3.x
except ImportError:
    import ConfigParser as configparser  # Python 2.x


class ApplicationConfig(configparser.ConfigParser):
    """ """
    def __init__(self, file_path):
        configparser.ConfigParser.__init__(self)
        self._file_path = file_path
        if file_path is not None:
            self.read(file_path)

    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d

    def __str__(self):
        return 'ApplicationConfig("{path}")'.format(path=self._file_path)

    def __repr__(self):
        return self.__str__()
