from pathlib import Path

from ..core import Task


class rename_replace(Task):
    def __init__(self, substring, replacement):
        self.substring = substring
        self.replacement = replacement

    def process(self, inputs):
        for t, c in inputs:
            t2 = Path(str(t).replace(self.substring, self.replacement))
            yield t2, c


class strip_dirs(Task):
    """
    Flattens file names, by stripping off directory components from the files
    and keeping only the base names.

    Modifies target filenames.
    Does not modify stream contents.

    Example::

        foo.js               =>  foo.js
        foo/bar/baz/quux.js  =>  quux.js

    .. warning::
       Be aware that stripping off directory components may result in
       duplicate file names, for example ``foo/qux.js`` and ``bar/qux.js``
       both rename their target to ``qux.js``, which is fine while still
       processing the stream, but will result in undefined behaviour when
       writing the stream output to disk.
    """
    def process(self, inputs):
        for t, c in inputs:
            t2 = Path(t.name)
            yield t2, c
