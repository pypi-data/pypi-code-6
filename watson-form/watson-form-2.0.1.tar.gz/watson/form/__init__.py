# -*- coding: utf-8 -*-
__version__ = '2.0.1'

try:
    # Fix for setup.py version import
    from watson.form.types import Form, Multipart

    __all__ = ['Form', 'Multipart']
except:  # pragma: no cover
    pass  # pragma: no cover
