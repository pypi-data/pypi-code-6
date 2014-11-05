import json
import logging
import os


def get_config_path():
    """
    Get's the path of the config json file
    """
    return get_path(CONFIG_FILE)


def write_config(token, app_key):
    """
    Write the BigPanda json config
    """
    with open(get_config_path(), 'w') as config_file:
        config_file.write(json.dumps({
            'app_key': app_key,
            'token':    token,
            'api_server':   'https://api.bigpanda.io',
            'post_path':    '/data/v2/alerts',
            }))


def read_config():
    """
    Read the BigPanda Splunk json config
    """
    with open(get_config_path()) as config_file:
        return json.load(config_file)


def get_path(path):
    """
    Get a path within the SPLUNK_HOME scripts folder
    """

    return os.path.join(SPLUNK_HOME, SCRIPT_PATH, path)


def setup_logging():
    """
    Setup logging to log file in Splunk script folder
    """
    logging.basicConfig(
        filename=get_path(LOG_FILE),
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


LOG = logging.getLogger("BigPanda Splunk")
SCRIPT_PATH = "bin/scripts"
CONFIG_FILE = 'bigpanda-splunk.json'
LOG_FILE = 'bigpanda-splunk.log'
SCRIPT_NAME = 'bigpanda-splunk'
SPLUNK_HOME = os.environ.get("SPLUNK_HOME", '/opt/splunk')
