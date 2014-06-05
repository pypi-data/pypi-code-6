# -*- coding: utf-8 -*-
"""finucane.apputils.errors

Provides both exceptions used by the Apputils modules, and exception which are
intended for use by a developer working with the Apputils framework.

.. note: Apputils modules may still raise standard exceptions, so be careful!

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


class ApputilsError (Exception):
    """The root of all Apputils internal evil."""
    pass


class ApputilsParseError(ApputilsError):
    """Raised by any Apputils parser when a parse has flown off of a cliff."""
    pass


class ApplicationError(Exception):
    """ Raised by a developer's application instance when an error occurs."""
    pass
