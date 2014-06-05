# -*- coding: utf-8 -*-
"""finucane.apputils.namespace

Provides the ``Namespace`` class.

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
from __future__ import (absolute_import, division, print_function, unicode_literals)
from finucane.apputils.compatibility import upgrade_namespace
upgrade_namespace(globals())


__all__ = ("Namespace", "as_namespace")

from collections import Mapping, Sequence, defaultdict

from .errors import ApputilsError


class NamespaceError(ApputilsError):
    pass


class NamespaceNotMutableError(NamespaceError):
    pass


class Namespace(object):
    """A dict subclass that exposes its items as attributes.

    Warning: Namespace instances do not have direct access to the
    dict methods.
    """

    def __init__(self, default_factory=None, data=None):
        if default_factory is None:
            default_factory = lambda: None
        if data is None:
            data = {}
        # using ``super`` (especially from ``future``) can be tricky in this case (so don't use it)!
        super_ = object
        super_.__init__(self)
        self.__dict__ = defaultdict(default_factory, data)

    def __dir__(self):
        return self.__dict__.dir()

    def __repr__(self):
        return "%s(%s)" % (type(self).__name__, sorted(dict(self.__dict__)))

    def __getattribute__(self, item):
        # using ``super`` (especially from ``future``) can be tricky in this case (so don't use it)!
        super_ = object
        if str(item).startswith('__'):
            return super_.__getattribute__(self, item)
        return super_.__getattribute__(self, '__dict__')[item]


class ImmutableNamespace(Namespace):
    """
    """
    def __setitem__(self, key, value):
        raise NamespaceNotMutableError('Cannot mutate non-mutable Namespace!')

    def __setattr__(self, name, value):
        if name in ['__dict__']:
            super().__setattr__('__dict__', value)
        else:
            raise NamespaceNotMutableError('Cannot mutate non-mutable Namespace!')

    def __delattr__(self, name):
        if name in ['__dict__']:
            self.__dict__ = None
        else:
            raise NamespaceNotMutableError('Cannot mutate non-mutable Namespace!')
