"""
Configuration Options
"""
import ConfigParser
import optparse
import logging
import socket
import os
from version import VERSION, PACKAGE


def get_config_dir():
    return os.path.join(
        os.environ['HOME'], '.config', 'zeropos', VERSION.rsplit('.', 1)[0]
    )


if not os.path.isdir(get_config_dir()):
    os.makedirs(get_config_dir(), 0700)


class ConfigManager(object):
    "Config manager"

    def __init__(self):
        self.defaults = {
            'port': 4000,
            'address': self.discover_local_ip(),
            'vendor': 0x04b8,
            'product': 0x0202,
            'interface': 0,
        }
        self.config = {}
        self.options = {}
        self.arguments = []

    def parse(self):
        parser = optparse.OptionParser(
            version=("%s %s" % (PACKAGE, VERSION)),
            usage="Usage: %prog [options]"
        )
        parser.add_option(
            "-c", "--config", dest="config",
            help="specify alternate config file"
        )
        parser.add_option(
            "-v", "--verbose", action="store_true",
            default=False, dest="verbose",
            help="logging everything at INFO level"
        )
        parser.add_option(
            "-l", "--log-level", dest="log_level",
            help="specify the log level: "
            "DEBUG, INFO, WARNING, ERROR, CRITICAL"
        )
        parser.add_option(
            "-a", "--address", dest="address",
            help="Address to bind to eg: 192.168.2.3"
        )
        parser.add_option(
            "-p", "--port", dest="port", type="int",
            help="specify the port to listen on"
        )

        opt, self.arguments = parser.parse_args()

        if len(self.arguments):
            parser.error('Too many arguments')

        if opt.config and not os.path.isfile(opt.config):
            parser.error('File "%s" not found' % (opt.config,))

        if opt.address:
            self.options['address'] = opt.address

        if opt.port:
            self.options['port'] = opt.port

        self.rcfile = opt.config or os.path.join(
            get_config_dir(), 'zeropos.conf'
        )
        self.load()

        logging.basicConfig()
        loglevels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL,
        }
        if not opt.log_level:
            if opt.verbose:
                opt.log_level = 'INFO'
            else:
                opt.log_level = 'ERROR'
        logging.getLogger().setLevel(loglevels[opt.log_level.upper()])

    def save(self):
        try:
            configparser = ConfigParser.ConfigParser()

            if not configparser.has_section('zeropos'):
                configparser.add_section('zeropos')

            for entry in self.config.keys():
                configparser.set('zeropos', entry, self.config[entry])

            configparser.write(open(self.rcfile, 'wb'))
        except IOError:
            logging.getLogger(__name__).warn(
                'Unable to write config file %s!'
                % (self.rcfile,))
            return False
        return True

    def load(self):
        configparser = ConfigParser.ConfigParser()
        configparser.read([self.rcfile])

        if not configparser.has_section('zeropos'):
            return

        for (name, value) in configparser.items('zeropos'):
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            if name in ('port', 'vendor', 'product', 'interface'):
                value = int(value)
            self.config[name] = value
        return True

    def __setitem__(self, key, value, config=True):
        self.options[key] = value
        if config:
            self.config[key] = value

    def __getitem__(self, key):
        """
        First look in options, then in config and then in defaults
        """
        return self.options.get(
            key, self.config.get(
                key, self.defaults.get(key)
            )
        )

    def discover_local_ip(self):
        """
        Try to find the local IP address and return it
        """
        rv = socket.gethostbyname(socket.gethostname())
        print("Discovered IP: %s" % rv)
        return rv


CONFIG = ConfigManager()
