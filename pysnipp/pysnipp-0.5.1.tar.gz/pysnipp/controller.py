import redis
import fileinput
import configparser
import os
from sys import exit

def connect(host='localhost',  port=6379, db=0, password=None,):
    if get_config():
        configfile = get_config()
        config = configparser.ConfigParser()
        config.read(configfile)
        host, port, db, password = config['STORAGE'].values()


    try:
        r = redis.StrictRedis(host, port, db, password)
        r.keys('*')
    except redis.exceptions.ConnectionError:
        print("ERROR: couldn't connect to redis")
        exit(1)
    return r

def list_snippets_w_content(expression='*'):
    r = connect()
    if expression is not '*':
        expression = "*%s*" % expression
    snippets = r.keys(expression)
    if snippets:
        for snippet in snippets:
            category, title = snippet.decode().split(':')
            print("\033[4m%s(%s):\033[0m" % (title, category)),
            for line in r.get(snippet).decode().split("\n"):
                print("\t %s" % line)
            print("\n")
    else:
       print('You have no snippets... for now ;)')

def list_snippets(expression='*'):
    r = connect()
    if expression is not '*':
        expression = "*%s*" % expression
    snippets = r.keys(expression)
    if snippets:
        for snippet in snippets:
            category, title = snippet.decode().split(':')
            print("%s(%s)" % (title, category)),
    else:
       print('You have no snippets... for now ;)')

def get_config():
    userfile = os.path.expanduser('~/.pysnipprc')
    globalfile = '/etc/pysnipprc'
    if os.path.isfile(userfile):
        return userfile
    elif os.path.isfile(globalfile):
        return globalfile
    else:
        return False




