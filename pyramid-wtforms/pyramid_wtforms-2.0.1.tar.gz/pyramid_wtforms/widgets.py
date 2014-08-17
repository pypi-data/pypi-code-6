from wtforms.widgets import *

class MultiFilesInput:
    """
    Renders multiple files input chooser field.
    """

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('multiple', 'multiple')
        return HTMLString('<input %s>' % html_params(name=field.name, type='file', **kwargs))
