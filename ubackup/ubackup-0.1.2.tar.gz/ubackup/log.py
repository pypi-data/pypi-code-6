import logging

# Import correct dictConfig depending on the Python version
try:
    from logging.config import dictConfig
except ImportError:
    from logutils.dictconfig import dictConfig


def level_names():
    levels = logging._levelNames.items()
    levels = map(lambda (k, v): v if isinstance(k, int) else None, levels)
    return filter(None, levels)


def set_level(level_name):
    # logging.getLogger().setLevel(level_name)
    for handler in logging.getLogger().handlers:
        handler.setLevel(level_name)


def set_config(config):
    dictConfig(config)
