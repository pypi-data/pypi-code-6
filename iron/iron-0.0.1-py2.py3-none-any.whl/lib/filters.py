from ..core import Task


class match(Task):
    """Filters only matching files."""

    def __init__(self, pattern):
        self.pattern = pattern

    def process(self, inputs):
        for t, c in inputs:
            if t.match(self.pattern):
                yield t, c


class exclude(Task):
    """Excludes matching files."""

    def __init__(self, pattern):
        self.pattern = pattern

    def process(self, inputs):
        for t, c in inputs:
            if not t.match(self.pattern):
                yield t, c
