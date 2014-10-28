import json
import logging

import serial

from .publishers.httppublisher import HttpPublisher
from .units.rfd21733.reader import Reader as SourceReader
from ._version import __version__

class HtDataClient:
    def __init__(self, device_path, publish_url, log_level='debug'):
        self.device_path = device_path
        self.publish_url = publish_url

        logger = logging.getLogger('htdataclient')

        level = getattr(logging, log_level.upper())
        logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        logger.addHandler(ch)

        self.logger = logger


    def publish(self, data):
        if not self.publish_url:
            return

        publisher = HttpPublisher(self.publish_url)
        try:
            response = publisher.publish(data)
            self.logger.info(response)
        except ConnectionRefusedError as e:
            self.logger.warn(e.strerror)

    def run(self):
        self.logger.debug('Hit reader is running')
        try:
            with serial.serial_for_url(self.device_path) as io_dev:
                for hit in SourceReader(io_dev):
                    self.logger.info(json.dumps(hit, sort_keys=True))
                    self.publish(hit)
        except serial.serialutil.SerialException as e:
            self.logger.debug(e)
        except KeyboardInterrupt:
            pass

def runner():
    import argparse
    parser = argparse.ArgumentParser(description='View and publish incoming hits to a target url')
    parser.add_argument('source_path', type=str, help='Path to the input source')
    parser.add_argument('publish_url', type=str, nargs='?', help='Path to target url')
    parser.add_argument('--log-level', type=str, help='Log level', default='info')
    # TODO: do something with --verbose
    #parser.add_argument('-v', '--verbose', action='store_true', default='Show all output')
    parser.add_argument('-V', '--version', action='version', version="%(prog)s " + __version__)
    args = parser.parse_args()

    reader = HtDataClient(args.source_path, args.publish_url, args.log_level)
    reader.run()
