#!/usr/bin/env python
# encoding: utf-8
import re
import plistlib


ANSI_COLOR_R = re.compile('^Ansi ([0-9]+) Color', re.I)
ANSI_TO_STANDARD_MAP = {
    0: 'black',
    1: 'red',
    2: 'green',
    3: 'yellow',
    4: 'blue',
    5: 'magenta',
    6: 'cyan',
    7: 'white',
    8: 'bright-black',
    9: 'bright-red',
    10: 'bright-green',
    11: 'bright-yellow',
    12: 'bright-blue',
    13: 'bright-magenta',
    14: 'bright-cyan',
    15: 'bright-white'
}

MISC_KEYS = {
    'Background Color': 'bg',
    'Foreground Color': 'fg'
}


def iterm_to_standard(iterm):
    parsed_file = plistlib.readPlistFromString(iterm)

    parsed_colors = {}
    for k, v in parsed_file.iteritems():
        is_ansi = ANSI_COLOR_R.match(k)
        if is_ansi:
            k = int(is_ansi.group(1))
            try:
                k = ANSI_TO_STANDARD_MAP[k]
            except KeyError:
                continue
        elif k in MISC_KEYS:
            k = MISC_KEYS[k]
        else:
            continue

        parsed_colors[k] = (
            int(v['Red Component'] * 255.0),
            int(v['Green Component'] * 255.0),
            int(v['Blue Component'] * 255.0)
        )

    return parsed_colors


def iterm_to_css(iterm, prefix='omt'):
    standard = iterm_to_standard(iterm)

    for key, rgb in standard.iteritems():
        yield (
            '.{prefix}-{key}-fg {{'
            'color: rgb({c[0]}, {c[1]}, {c[2]});'
            '}}'
        ).format(prefix=prefix, key=key, c=rgb)
        yield (
            '.{prefix}-{key}-bg {{'
            'background-color: rgb({c[0]}, {c[1]}, {c[2]});'
            '}}'
        ).format(prefix=prefix, key=key, c=rgb)
