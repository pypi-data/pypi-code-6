import os
try:
    from configparser import SafeConfigParser, NoOptionError, DuplicateSectionError
except ImportError:
    from ConfigParser import SafeConfigParser, NoOptionError, DuplicateSectionError

class Config(SafeConfigParser):

    default_sections = ('java',)
    __instances = {} # cqs_home -> Config() object

    def __init__(self, cqs_home=None):
        if cqs_home is None:
            cqs_home = os.path.join(os.path.expanduser("~"),'.cassandra-quickstart')
        self.__cqs_home = cqs_home
        self.__cfg_path = os.path.join(cqs_home, 'config')

        if self.__cfg_path in self.__instances.keys():
            raise ValueError("Config already open for {cqs_home}. Use Config.open() instead.".format(cfg_path=self.__cqs_home))

        SafeConfigParser.__init__(self)
        self.read(self.__cfg_path)

        for s in self.default_sections:
            self.add_section(s)

        self.__instances[self.__cqs_home] = self

    def add_section(self, section):
        """Add section, don't complain if it already exists"""
        try:
            SafeConfigParser.add_section(self, section)
        except DuplicateSectionError:
            pass
        
    def save(self):
        with open(self.__cfg_path, 'wb') as f:
            self.write(f)

    @staticmethod
    def open(cqs_home=None):
        if cqs_home is None:
            cqs_home = os.path.join(os.path.expanduser("~"),'.cassandra-quickstart')
        try:
            return Config.__instances[cqs_home]
        except KeyError:
            return Config(cqs_home)
