import ConfigParser
import os

BASE_URL_V1 = 'https://bitbucket.org/api/1.0/'
BASE_URL_V2 = 'https://bitbucket.org/api/2.0/'

CFGFILE = os.path.join(os.path.expanduser('~'), '.b2tool')

def get_or_default(config, section, key, default=''):
    try:
        return config.get(section, key)
    except ConfigParser.NoSectionError:
        return default
    except ConfigParser.NoOptionError:
        return default

def get_credentials():
    if os.path.isfile(CFGFILE):
        conf = ConfigParser.SafeConfigParser()
        conf.read(CFGFILE)
        username = get_or_default(conf, 'AUTH', 'username')
        password = get_or_default(conf, 'AUTH', 'password')

        return username,password
    else:
        return '',''