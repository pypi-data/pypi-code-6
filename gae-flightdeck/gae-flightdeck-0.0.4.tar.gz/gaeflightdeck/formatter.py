#!/usr/bin/env python

import sys
import re
import colorama


COLORS = {
    'DEBUG': colorama.Fore.CYAN + colorama.Back.RESET,
    'INFO': colorama.Fore.BLUE + colorama.Back.RESET,
    'WARNING': colorama.Fore.YELLOW + colorama.Back.RESET,
    'ERROR': colorama.Fore.RED + colorama.Back.RESET,
    'CRITICAL': colorama.Fore.RED + colorama.Back.YELLOW,
}

LEVELS = COLORS.keys()


def format_log(parts):
    level = parts[0]
    date = ' '.join(parts[1:3])
    file = parts[3]
    message = ' '.join(parts[4:])
    color = COLORS[level]

    return ' '.join([color, level, colorama.Fore.MAGENTA, colorama.Back.RESET, date, colorama.Style.BRIGHT, file, colorama.Style.RESET_ALL, message])


def filter_logs(parts):
    if ' '.join(parts[4:]) == "Stripped prohibited headers from URLFetch request: ['content-length']":
        return False
    return True


def process_log(line, output_func=None):
    line = line.rstrip()
    parts = re.split('\s+', line)

    if parts[0] in LEVELS:
        if filter_logs(parts):
            print format_log(parts)
            if output_func:
                output_func(line)
        else:
            return
    else:
        print line
        if output_func:
            output_func(line)
