# -*- coding: utf-8 -*-
from nose.plugins import Plugin
from .poserbox import PoserBox
import os

DEFAULT_PORT_ENVVAR = 'POSERBOX_PORT'


class PoserBoxPlugin(Plugin):

    """A nose plugin that sets up a sandboxed poser instance."""

    name = 'poserbox'

    def options(self, parser, env):
        super(PoserBoxPlugin, self).options(parser, env)
        parser.add_option(
            "--poserbox-bin",
            dest="bin",
            action="store",
            default=None,
            help="Optionally specify the path to the poser executable.")
        parser.add_option(
            "--poserbox-port",
            action="store",
            dest="port",
            type="int",
            default=0,
            help="Optionally specify the port to run poser on.")
        parser.add_option(
            "--poserbox-scenesfile",
            action="store",
            dest="scenesfile",
            default=None,
            help=("Path to scenes file (yaml or json)."))
        parser.add_option(
            "--poserbox-port-envvar",
            action="store",
            dest="port_envvar",
            default=DEFAULT_PORT_ENVVAR,
            help=("Which environment variable dynamic port number will be "
                  "exported to."))

    def configure(self, options, conf):
        super(PoserBoxPlugin, self).configure(options, conf)

        if not self.enabled:
            return

        self.poserbox = PoserBox(
            poser_bin=options.bin, port=options.port or None,
            scenes_file=options.scenesfile
        )

        self.port_envvar = options.port_envvar

    def begin(self):
        assert self.port_envvar not in os.environ, (
            '{} environment variable is already taken. Do you have other '
            'tests with poserbox running?'.format(self.port_envvar))

        self.poserbox.play()
        os.environ[self.port_envvar] = str(self.poserbox.port)

    def finalize(self, result):
        self.poserbox.stop()
        del os.environ[self.port_envvar]
