import ConfigParser
import sys

import komandr

import requests
from b2tool import __projectname__
from b2tool.conf import CFGFILE, BASE_URL_V1


_auth = komandr.prog(prog='{0} auth'.format(__projectname__))

@komandr.command
@komandr.arg('cmd', 'cmd', choices=['login', 'logout'], help="Available auth subcommands. Use <subcommand> -h to see more.")
def auth(cmd):
    _auth.execute(sys.argv[2:])

@_auth.command
@_auth.arg('username', required=True, type=str, help='')
@_auth.arg('password', required=True, type=str, help='')
def login(username=None, password=None):

    path = BASE_URL_V1 + 'user/'
    res = requests.get(path, auth=(username, password))
    print 'Logging...'
    if res.status_code == 200:
        with open(CFGFILE, 'wb') as cfg:
            conf = ConfigParser.ConfigParser()
            conf.add_section('AUTH')
            conf.set('AUTH', 'username', username)
            conf.set('AUTH', 'password', password)
            conf.write(cfg)
            print "Login successful!"
        return True
    else:
        print "Username or password invalid."
        return False

def logout():
    pass