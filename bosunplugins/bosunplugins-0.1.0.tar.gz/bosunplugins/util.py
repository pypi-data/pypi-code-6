import re

from bosun import network


uuid_re = re.compile(r'[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}')

def is_uuid(text):
    """ Test if the text is a UUID or not """
    return bool(uuid_re.match(text))


# provide access to network.get_my_host here
get_my_host = network.get_my_host
