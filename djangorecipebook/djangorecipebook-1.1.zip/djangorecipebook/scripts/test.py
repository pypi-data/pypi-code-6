"""
Recipe generating a test script
"""

from .manage import manage_main


def main(settings_module, *args):
    manage_main(settings_module, 'test', *args)
