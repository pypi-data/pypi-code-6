NAME = 'local1'

# AWS, SQS
region = ''
id = ''
key = ''
queue_prefix = 'dev_prorab_'
general_queue = queue_prefix + 'general'
personal_queue = queue_prefix + NAME


# Auth
ACCESS_TOKEN = 'foobar'


dir = '.'


# Server
WEBSOCKET_PORT = 8099


# Timing things
SEND_OUT = 1
PULL_QUEUE = 2
IO_THREAD = 0.5
PING = 1

try:
    exec(open('/etc/prorab.py').read())
except IOError:
    pass

