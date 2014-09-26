import io
import ConfigParser
from os.path import expanduser
from os.path import join


class TestingUtils(object):

    @staticmethod
    def get_test_config():

        sample_config = """
[jenkins]
server-job=XL Deploy (master)
url=https://somehost.com
username=bla
password=blabla
[deployit]
username=admin
password=admin
protocol=http
host=localhost
port=4516
"""
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.read([join(expanduser("~"), '.xl-helper')])
        config.readfp(io.BytesIO(sample_config))
        return config
