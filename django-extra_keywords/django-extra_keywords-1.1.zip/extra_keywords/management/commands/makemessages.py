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

from django.core.management.commands import makemessages as makemessages_core
from django.core.management.base import CommandError
from django.conf import settings

try:
    # django >= 1.6
    from django.core.management.utils \
    import popen_wrapper as popen_wrapper_core
    _popen_core = None
except ImportError:
    # django < 1.6
    from django.core.management.commands.makemessages \
    import _popen as _popen_core
    popen_wrapper_core = None


class Command(makemessages_core.Command):

    option_list = makemessages_core.Command.option_list + (
        make_option('--extra-keyword', dest='extra_keywords', action='append',
            default=[],
            help='If you use import aliases for ugettext and its variations, '
                 'you can specify them here to make sure that xgettext will '
                 'find your translatable strings.'),)

    def handle_noargs(self, **options):

        extra_keywords = set(options.pop('extra_keywords'))
        extra_keywords.update(getattr(settings, 'GETTEXT_EXTRA_KEYWORDS', ()))

        if popen_wrapper_core:
            def popen_wrapper_xtra_kw(args, os_err_exc_type=CommandError):
                if args and args[0] == 'xgettext':
                    for kw in extra_keywords:
                        args.append('--keyword=%s' % kw)
                return popen_wrapper_core(args, os_err_exc_type)

            makemessages_core.popen_wrapper = popen_wrapper_xtra_kw
        else:
            def _popen_xtra_kw(cmd):
                to_insert = ''
                if cmd.startswith('xgettext') and '--keyword' in cmd:
                    for kw in  extra_keywords:
                        to_insert += ' --keyword=%s' % kw
                    if to_insert:
                        i = cmd.find(' ', cmd.rfind('--keyword'))
                        cmd = cmd[:i] + to_insert + cmd[i:]
                return _popen_core(cmd)
            makemessages_core._popen = _popen_xtra_kw

        try:
            super(Command, self).handle_noargs(**options)
        finally:
            # restore popen_wrapper or _popen
            if popen_wrapper_core:
                makemessages_core.popen_wrapper = popen_wrapper_core
            else:
                makemessages_core._popen = _popen_core
