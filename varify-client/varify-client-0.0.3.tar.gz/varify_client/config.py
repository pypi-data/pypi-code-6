import ConfigParser
import os
from sys import stderr

class ConnectionConfig:
    host = None
    port = None
    protocol = None
    token = None
    def reset(self):
        self.host = None
        self.port = None
        self.protocol = None
        self.token = None

configPath = None

def updateConfigPath(newPath):
    import config
    config.configPath = os.path.join(os.getcwd(), os.path.expanduser(newPath))

updateConfigPath('varify.cfg')

connectionConfig = ConnectionConfig()

def readConfig():
    connectionConfig.reset()
    parser = ConfigParser.ConfigParser()
    try:
        parser.readfp(open(configPath))
    except IOError, e:
        print >> stderr, "Can't find config file \"" + configPath + "\"; using default settings"
    if parser.has_section('Connection'):
        if parser.has_option('Connection', 'host'):
           connectionConfig.host = parser.get('Connection', 'host')
        if parser.has_option('Connection', 'port'):
           connectionConfig.port = parser.getint('Connection', 'port')
        if parser.has_option('Connection', 'protocol'):
           connectionConfig.protocol = parser.get('Connection', 'protocol')
        if parser.has_option('Connection', 'token'):
           connectionConfig.token = parser.get('Connection', 'token')

    if (connectionConfig.port == None): connectionConfig.port = 80
    if (connectionConfig.host == None): connectionConfig.host = '127.0.0.1'
    if (connectionConfig.protocol == None): connectionConfig.protocol = 'http'