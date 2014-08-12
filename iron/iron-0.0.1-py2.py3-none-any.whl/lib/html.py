from htmlmin import Minifier

from ..core import Task


class minify_html(Task):
    """Minifies HTML input files."""

    def __init__(self, *htmlmin_args, **htmlmin_kwargs):
        self.minifier = Minifier(*htmlmin_args, **htmlmin_kwargs)

    def lazy_minify(self, contents):
        yield self.minifier.minify(b''.join(contents).decode('utf-8')).encode('utf-8')

    def process(self, inputs):
        for t, c in inputs:
            yield t, self.lazy_minify(c)
