#
# Copyright (c) 2010, 2014
#  Adam Tauno Williams <awilliam@whitemice.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE
#
import time
import sys
from coils.core.logic import ActionCommand


class AbendAction(ActionCommand):

    """
    This action fails, on purpose, the point is to fail.

    In Do this action sleeps for 4 seconds then causes an OS process exit
    with a result status of 4.  Why 4?  who knows, this could certainly be
    improved.
    """

    __domain__ = "action"
    __operation__ = "abend"
    __aliases__ = ['abendAction', ]
    mode = None

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        """Perform the action - sleep for 4 seconds then OS exit."""
        time.sleep(4)
        sys.exit(4)
