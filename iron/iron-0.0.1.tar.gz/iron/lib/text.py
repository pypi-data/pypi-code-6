import re
from itertools import chain

from more_itertools import flatten

from pathlib import Path

from ..core import Task


class concat(Task):
    """
    Concatenates input stream contents to the given output file, in the order
    that they appear in the inputs.

    Modifies target filename.
    Modifies stream contents.

    Example::

        foo.js, bar.js, qux.js  =>  all.js

    """
    def __init__(self, dest):
        self.dest = Path(dest)

    def process(self, inputs):
        yield self.dest, flatten(chain(c for _, c in inputs))


class contents_replace(Task):
    def __init__(self, substring, replacement):
        self.substring = substring
        self.replacement = replacement

    def lazy_replace(self, c):
        contents = b''.join(c).decode('utf-8').replace(self.substring, self.replacement).encode('utf-8')
        yield contents

    def process(self, inputs):
        for t, c in inputs:
            yield t, self.lazy_replace(c)


class footer(Task):
    def __init__(self, bites):

        if isinstance(bites, str):
            bites = bites.encode('utf-8')
        if not isinstance(bites, bytes):
            raise TypeError('expected bytes')
        self.bites = bites

    def process(self, inputs):
        for t, c in inputs:
            yield t, chain(c, [self.bites])


class header(Task):
    def __init__(self, bites):

        if isinstance(bites, str):
            bites = bites.encode('utf-8')
        if not isinstance(bites, bytes):
            raise TypeError('expected bytes')
        self.bites = bites

    def process(self, inputs):
        for t, c in inputs:
            yield t, chain([self.bites], c)


class regex(Task):
    def __init__(self, pattern, replacement):
        self.pattern = pattern
        self.replacement = replacement
        self.regex = re.compile(self.pattern, re.MULTILINE)

    def process(self, inputs):
        for t, c in inputs:
            c2 = self.regex.sub(self.replacement, b''.join(c).decode('utf-8'))
            yield t, [c2.encode('utf-8')]
