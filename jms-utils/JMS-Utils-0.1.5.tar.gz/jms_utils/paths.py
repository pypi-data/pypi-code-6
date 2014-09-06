import logging
import os

log = logging.getLogger(__name__)


class ChDir(object):
    # Step into a directory temporarily. Then return to
    # orignal directory.
    def __init__(self, path):
        self.old_dir = os.getcwd()
        self.new_dir = path

    def __enter__(self):
        log.debug(u'Changing to Directory --> {}'.format(self.new_dir))
        os.chdir(self.new_dir)

    def __exit__(self, *args):
        log.debug(u'Moving back to Directory --> {}'.format(self.old_dir))
        os.chdir(self.old_dir)
