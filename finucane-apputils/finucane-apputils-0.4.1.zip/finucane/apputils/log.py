# -*- coding: utf-8 -*-
"""finucane.apputils.log

Provides customized application logging facilities and utilities. If a
customized or enhanced application logging ability is needed, this is where it
should exist.

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

import logging
import json


class JsonFormatter(logging.Formatter):
    """
    """
    def format(self, record):
        """ """
        return json.dumps(vars(record), indent=1)


class LogAboveErrorFilter(logging.Filter):
    """
    """
    def __init__(self):
        logging.Filter.__init__(self)

    def filter(self, record):
        # CRITICAL = 50
        # ERROR = 40
        # WARNING = 30
        # INFO = 20
        # DEBUG = 10
        # NOTSET = 0
        if record.levelno < logging.ERROR:
            return 1
        else:
            return 0
