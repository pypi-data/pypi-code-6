# -*- coding: utf-8 -*-
"""finucane.apputils.compatibility

Provides facilities for making code cross-platform, cross-python, etc.
Code compatibility is the focus here. As always, things should "just work."

Notably, this module provides utilities for making code/modules capable of
being run in older versions of Python (herein: ``yesterpy``).

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
from future.builtins import (bytes, dict, int, list, object, range, str,
                             ascii, chr, hex, input, next, oct, open,
                             pow, round, super, filter, map, zip)

import sys

__python_version__ = dict()
try:
    __python_version__['major'] = sys.version_info.major
except AttributeError:
    __python_version__['major'] = sys.version_info[0]
try:
    __python_version__['minor'] = sys.version_info.minor
except AttributeError:
    __python_version__['minor'] = sys.version_info[1]

__upgraded__ = ['bytes', 'dict', 'int', 'list', 'object', 'range', 'str',
                 'ascii', 'chr', 'hex', 'input', 'next', 'oct', 'open',
                 'pow', 'round', 'super', 'filter', 'map', 'zip']


def upgrade_namespace(namespace):
    """Applies upgrades to allow code in namespace to run in earlier Python interpreters.

    .. warning: The specified namespace will be modified!
    .. note: The specified namespace must be modifiable for this to be
    effective.

    After this function is called on a namespace, Python 3.x flavored code will
    generally be able to be executed by a Python 2.6 or greater interpreter.

    Example::

        from finucane.apputils.compatibility import upgrade_namespace
        upgrade_namespace(globals())

    Args:
        namespace: A namespace instance (dict, usually the return value of
        ``globals()``)

    Returns:
        None
    """
    namespace['future'] = __import__('future', globals=namespace,
                                     fromlist=[], level=0)
    enhanced_ = __import__('future.builtins', globals=namespace,
                           fromlist=__upgraded__, level=0)

    for import_name in __upgraded__:
        namespace[import_name] = getattr(enhanced_, import_name)

    if 'unicode' not in namespace:
        namespace['unicode'] = namespace['str']

    namespace['__python_version__'] = __python_version__
