"""
There were 2 options to add arguments to xgettext
1. add arguments to the list built in process function, this would require
   copying the function and adding 3 lines to it ...
2. add arguments afterwards, when popen_wrapper is called, by
   monkey-patching the popen_wrapper function

Given the size of this file, you have probably guessed that it's the
2nd solution that is used here

(c) 2014 Thomas Khyn
MIT license (see LICENSE.txt)
"""

from optparse import make_option

from django.core.management.utils import popen_wrapper as popen_wrapper_core
from django.core.management.commands import makemessages as makemessages_core
from django.core.management.base import CommandError


class Command(makemessages_core.Command):

    option_list = makemessages_core.Command.option_list + (
        make_option('--extra-keywords', dest='extra_keywords', action='append',
            default=[],
            help='If you use import aliases for ugettext and its variations, '
                 'you can specify them here to make sure that xgettext will '
                 'find your translatable strings.'),)

    def handle_noargs(self, **options):

        extra_keywords = options.pop('extra_keywords')

        def popen_wrapper_xtra_kw(args, os_err_exc_type=CommandError):
            if args and args[0] == 'xgettext':
                for kw in extra_keywords:
                    args.append('--keyword=%s' % kw)
            return popen_wrapper_core(args, os_err_exc_type)

        makemessages_core.popen_wrapper = popen_wrapper_xtra_kw

        try:
            super(Command, self).handle_noargs(**options)
        finally:
            # restore popen_wrapper
            makemessages_core.popen_wrapper = popen_wrapper_core
