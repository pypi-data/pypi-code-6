"""
Configuration file.
"""

import os
import re

import pkg_resources as pkg

from ConfigParser import SafeConfigParser as Parser
from ConfigParser import NoSectionError

from pkginfo import __title__
from logger import log


class DitzConfig(Parser):
    def __init__(self):
        Parser.__init__(self)
        defaults = pkg.resource_filename(__name__, "config.cfg")
        with open(defaults) as fp:
            self.readfp(fp)

    def write_file(self, path):
        """Write config data to file."""

        with open(path, "w") as fp:
            fp.write("# %s configuration file.\n\n" % __title__)
            self.write(fp)


class Config(object):
    def __init__(self):
        homedir = os.path.expanduser("~")
        self.path = os.path.join(homedir, ".ditzrc")
        self.parser = None

    def set_file(self, path):
        self.path = path

    def set_option(self, setting):
        m = re.match(r'(\w+)\.(\w+)=(.*)', setting)
        if m:
            section, option, value = m.groups()
        else:
            raise ValueError("'%s': expected 'section.option=value'"
                             % setting)

        try:
            self.set(section, option, value)
        except NoSectionError:
            raise ValueError("'%s': no such config section" % section)

    def __getattr__(self, attr):
        if not self.parser:
            self.parser = DitzConfig()
            log.info("reading %s" % self.path)
            self.parser.read(self.path)

        return getattr(self.parser, attr)


# Ditz user config settings.
config = Config()
