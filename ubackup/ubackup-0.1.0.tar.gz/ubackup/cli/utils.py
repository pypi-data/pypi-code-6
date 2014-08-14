import click
import sys
from dateutil import tz
from ubackup.utils import filesizeformat


def ask_for_rev(revisions):
    rev_to_restore = revisions[0]

    if len(revisions) > 1:
        to_zone = tz.tzlocal()
        for i, rev in enumerate(revisions):
            sys.stdout.write('%(i)2s. %(date)s: %(size)s\n' % {
                'i': i,
                'date': rev['date'].astimezone(to_zone).strftime('%Y-%m-%d %H:%M:%S'),
                'size': filesizeformat(rev['size'])
            })
        sys.stdout.flush()
        response = click.prompt(
            "Which version do you want to restore?",
            type=click.IntRange(min=0, max=len(revisions) - 1),
            prompt_suffix=' ')
        rev_to_restore = revisions[response]

    return rev_to_restore
