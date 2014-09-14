from ..core import Task


class markdown(Task):
    """Converts Markdown to HTML."""

    def __init__(self):
        try:
            from markdown import markdown as markdown_fn
        except ImportError as e:
            raise ImportError('To use markdown(), run: pip install markdown') from e

        self.convert = markdown_fn

    def lazy_convert(self, contents):
        yield self.convert(b''.join(contents).decode('utf-8')).encode('utf-8')

    def process(self, inputs):
        for t, c, m in inputs:
            t2 = t.with_suffix('.html')
            yield t2, self.lazy_convert(c), m
