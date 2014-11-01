DEBUG = True
SERVICE_NAME = 'wunderground'
SERVICE_VERSION = '0.1.0'
SERVICE_UUID = 'ef223574-0918-42c3-9117-64a1aa56c1a1'
SERVICE_DESCRIPTION = 'This service provides various commands for checking the weather'

WUNDERGROUND_API_KEY = "test"

##############################################################################
# The following setting defines a dictionary containing Redis connection
# information used when connecting to the Redis server.
#
# This setting is required.

REDIS_CONNECTION = {
    'host': '192.168.33.66',
    'port': 6379,
    'db': 0,
    'password': None,
}
##############################################################################


##############################################################################
# The following channel settings are for when you need to change the default
# Redis channel key for each pipe respectively. BROADCAST_SERVICE_CHANNEL
# is used for messages going from Tenyks to Redis for the clients.
# BROADCAST_ROBOT_CHANNEL is used for messages going from clients to Tenyks
# for IRC.
#
# These are namespaced, so you shouldn't need to change them.
#
# These settings are optional

BROADCAST_SERVICE_CHANNEL = 'tenyks.service.broadcast'
BROADCAST_ROBOT_CHANNEL = 'tenyks.robot.broadcast'
##############################################################################
