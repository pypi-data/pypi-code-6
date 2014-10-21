# Copyright 2011-2014 Arthur Noel
#
# This file is part of Yanc.
#
# Yanc is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Yanc is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Yanc. If not, see <http://www.gnu.org/licenses/>.

from nose.plugins import Plugin
from nose.result import TextTestResult

from yanc.colorstream import ColorStream

DO_YANC = False


# monkey patch TextTestResult.__init__ to wrap the out stream with ColorStream
def testresult_init(self, *args, **kwargs):
    self._real_init(*args, **kwargs)
    if DO_YANC:
        self.stream = ColorStream(self.stream)

TextTestResult._real_init = TextTestResult.__init__
TextTestResult.__init__ = testresult_init


class YancPlugin(Plugin):
    """Yet another nose colorer"""

    name = "yanc"

    _options = (
        ("color", "YANC color override - one of on,off [%s]", "store"),
    )

    def options(self, parser, env):
        super(YancPlugin, self).options(parser, env)
        for name, doc, action in self._options:
            env_opt = "NOSE_YANC_%s" % name.upper()
            parser.add_option("--yanc-%s" % name.replace("_", "-"),
                              action=action,
                              dest="yanc_%s" % name,
                              default=env.get(env_opt),
                              help=doc % env_opt)

    def configure(self, options, conf):
        super(YancPlugin, self).configure(options, conf)
        for name, dummy1, dummy2 in self._options:
            name = "yanc_%s" % name
            setattr(self, name, getattr(options, name))
        # multiprocess plugin workers will not have a stream on conf
        if hasattr(self.conf, "stream"):
            global DO_YANC
            DO_YANC = self.yanc_color != "off" \
                and (self.yanc_color == "on"
                     or (hasattr(conf.stream, "isatty")
                         and conf.stream.isatty()))
