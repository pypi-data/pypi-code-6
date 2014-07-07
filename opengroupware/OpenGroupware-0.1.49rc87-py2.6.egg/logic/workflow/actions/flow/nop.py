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
from coils.core.logic import ActionCommand

IO_BLOCK_SIZE = 4096


class NoActionAction(ActionCommand):

    """
    The noActionAction, or NOP, does nothing.

    It simply copies its input to its output;  generally this is only useful
    for testing, but it can have a practical purpose where the contents of a
    message needs to be *copied* from a message to a message with a specific
    label.
    """

    __domain__ = "action"
    __operation__ = "nop"
    __aliases__ = ['noAction', 'noActionAction', ]

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        """Do nothing but pass the data through, from rfile to wfile."""
        data = self.rfile.read(IO_BLOCK_SIZE)
        while data:
            self.wfile.write(data)
            data = self.rfile.read(IO_BLOCK_SIZE)

    def parse_action_parameters(self):
        """Parse action parameters; no paramters supported for this action."""
        pass
