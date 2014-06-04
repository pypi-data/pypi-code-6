# -*- coding: utf-8 -*-
"""finucane.apputils

Finucane-Apputils: The Finucane Research Application Framework.

This framework is intended for application developers; specifically, developers
of tools with command-line interfaces. This framework can be used to create
applications with GUIs, but does not provide any direct support for such
endeavors, at this time. Support for **rapid**, consistent GUI development, a
"connected code" foundation, and much more, are on the roadmap for this project.

Tools created with this framework gain a consistent interface foundation. In
other words, this framework provides an abstract base for applications so that
a developer can leverage the well-known advantages of inheritance.


http://finucane-apputils.readthedocs.org/en/latest/

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
from .application import Application
from .errors import ApplicationError

__all__ = ['Application', 'ApplicationError']
