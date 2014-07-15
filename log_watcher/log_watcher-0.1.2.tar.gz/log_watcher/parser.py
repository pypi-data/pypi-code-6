from datetime import datetime

import re

# -----------------------------------------------------------------------------

CURRENT_YEAR = datetime.now().year

# -----------------------------------------------------------------------------

class Parser(object):
    def __init__(self, file_path, regexp):
        self.file_path = file_path
        self.regexp = regexp

    def parse(self):
        # Infinite seeking, reproduce tail -f behavior by using a generator
        if not hasattr(self, '_pos'):
            self._pos = None
        with open(self.file_path, 'r') as fp:
            if self._pos is None:
                # Seek to end of file and store position
                fp.seek(0, 2)
                self._pos = fp.tell()
            else:
                # Seek to the last known position
                fp.seek(self._pos, 0)
                for line in fp:
                    if line != "\n" and not self.check_line(line):
                        yield line
                self._pos = fp.tell()

    def parse_datetime(self, line):
        raise NotImplementedError

    def check_line(self, line):
        raise NotImplementedError

# -----

class KernelParser(Parser):
    def check_line(self, line):
        if re.findall(self.regexp, line):
            return False
        else:
            return True
