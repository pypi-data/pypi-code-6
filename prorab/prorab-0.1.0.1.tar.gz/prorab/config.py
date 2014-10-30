NAME = 'local1'

# AWS, SQS
region = 'eu-west-1'
id = 'AKIAI3GEEITH7AMA5J4Q'
key = 'VsP4pGOQMqYh77O77l0pcJ0F6pJkPErnUb+KSm+K'
queue_prefix = 'dev_prorab_'
general_queue = queue_prefix + 'general'
personal_queue = queue_prefix + NAME


# Auth
ACCESS_TOKEN = 'foobar'


# Commands
commands = {
    'sf_invalid_emails': 'php symfony tasks:invalid-emails',
    'test': './test',
    'bang!': '',
}
dir = '.'
STDOUT_BUFFER_LENGTH = 32


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

