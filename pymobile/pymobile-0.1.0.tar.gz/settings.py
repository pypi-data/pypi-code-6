# debug-logging for development
debug = False


#cookies
max_age = 86400  # in seconds
secret_key = '96c8428b-b7af-46ed-913d-97a5f8e9ac94'  # secret signingkey for simple session.
username = 'root'
password = 'admin'

#web-server
host = '0.0.0.0'
port = 8080

#websocket-server
ws_host = host
ws_port = port + 1

try:
    from localsettings import *
except ImportError:
    pass