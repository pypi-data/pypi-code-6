__version__ = '0.1.0-alpha'

# Aaargh! setup requires django, but reads __version__
# there for ``import register`` crashes setup.py
try:
    import django  # noqa
except ImportError:
    pass
else:
    from .registry import register  # noqa
