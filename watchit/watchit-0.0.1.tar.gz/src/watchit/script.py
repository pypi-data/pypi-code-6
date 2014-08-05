"""watchit

Usage: watchit [<dir>]

Options:
  -h --help         Show this screen.

Watches a directory for any file change events and will exit on the first one
it encounters. "I'm walking here!"

"""

import sys

from docopt import docopt
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('watchit.script')

class EventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if not event.is_directory:
            logger.info("%s %s" % (event.event_type, event.src_path))
            sys.exit(0)

def main():
    args = docopt(__doc__)
    path = args.get('<dir>') or '.'

    observer = Observer()
    event_handler = EventHandler()

    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    observer.join()
    observer.unschedule_all()
    observer.stop()

if __name__ == "__main__":
    main()
