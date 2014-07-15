from log_watcher import validators
from log_watcher.parser import KernelParser
from log_watcher.tracker import CloudwatchTracker
from log_watcher.utils import get_hostname

import click
import time
# import os
import logging

# -----------------------------------------------------------------------------

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------

@click.command()
@click.option('--file-path', default='/tmp/kern.log', help='File path to watch.', callback=validators.file_path)
@click.option('--regexp', default=r'match-this-string', help='Regular expression to match.', callback=validators.regexp)
@click.option('--period', default=30, help='How many minutes to wait between checks.')
def main(file_path, regexp, period):
    # regexp=r'Not tainted|PAX: size overflow detected'
    logger.info('Initializing...')

    # Track Kernel log
    parser = KernelParser(file_path=file_path, regexp=regexp)
    tracker = CloudwatchTracker(name="%s_kernel_anomalies" % get_hostname(), period=period)

    while True:
        for line in parser.parse():
            tracker.track(1)

        # Make sure that we track an empty event each second
        tracker.track()
        time.sleep(1)

# -----

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(e, exc_info=True)
