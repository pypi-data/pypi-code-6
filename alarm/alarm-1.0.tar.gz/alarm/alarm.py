#!/usr/bin/python
# -*- coding: utf-8 -*-

# alarm.py

# Copyright 2014 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# CLI Alarm Clock

# https://github.com/dslackw/alarm

# Alarm is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import time

__all__ = "alarm"
__author__ = "dslackw"
__version_info__ = (1, 0)
__version__ = "{0}.{1}".format(*__version_info__)
__license__ = "GNU General Public License v3 (GPLv3)"
__email__ = "d.zlatanidis@gmail.com"

def start_ALARM(ALARM, SONG):
    '''
    All the work going on here. To the Authority the right time format
    and finding the correct path of the file. The Application requires
    Mplayer to play the alarm sound. Please read which sounds are supported 
    in page : 
    http://web.njit.edu/all_topics/Prog_Lang_Docs/html/mplayer/formats.html
    '''
    try:
        ALARM = ALARM.replace(":", " ").split() # split items
        for item in ALARM:
            if len(item) > 2 or len(item) == 1:
                print("Setting time pattern is 'HH:MM:SS'")
                sys.exit()
        if int(ALARM[0]) in range(0, 24):
            pass
        else:
            print("Error: hour out of range")
            sys.exit()
        if int(ALARM[1]) in range(0, 60):
            pass
        else:
            print("Error: minutes out of range")
            sys.exit()
        if int(ALARM[2]) in range(0, 60):
            pass
        else:
            print("Error: seconds out of range")
            sys.exit()
    except ValueError:
        print("Setting time pattern is 'HH:MM:SS'")
        sys.exit()
    if not os.path.isfile(SONG):
        print("Error: the file does not exist")
        sys.exit()
    ALARM = ":".join(ALARM) # reset begin format
    while True:
        try:
            os.system("clear")
            print("+" + "=" * 78 + "+")
            print("|" + " " * 30 + "CLI Alarm Clock" + " " * 33 + "|")
            print("+" + "=" * 78 + "+")
            print("| Alarm set at : %s" % ALARM + " " * (62-len(ALARM)) + "|")
            print("| Sound file in : %s" % SONG + " " * (61-len(SONG)) + "|")
            start_time = time.strftime("%H:%M:%S")
            print("| Time : %s" % start_time+ " " * (70-len(start_time)) + "|")
            print("+" + "=" * 78 + "+")
            time.sleep(0.1)
            if start_time == ALARM:
                os.system("mplayer '%s'" % SONG)
                break
        except KeyboardInterrupt:
            print("\nAlarm canceled!")
            break

def main():
    args = sys.argv
    args.pop(0)
    if len(args) == 0:
        print("try alarm --help")
    elif len(args) == 1 and args[0] == "-h" or args[0] == "--help":
        print("usage: %s [-h] [-v]" % __all__)
        print("             [-s] <time> <song>\n")
        print("optional arguments")
        print("  -h, --help       show this help message and exit")
        print("  -v, --version    print version and exit")
        print("  -s, --set        set time and sound")
        print("\nexample: alarm -s 06:00:00 /path/to/song.mp3") 
    elif len(args) == 1 and args[0] == "-v" or args[0] == "--version":
        print("Version : %s" % __version__)
    elif len(args) == 3 and args[0] == "-s" or len(args) == 3 and args[0] == "--set":
        start_ALARM(ALARM=args[1], SONG=args[2])
    else:
        print("try alarm --help")
        
if __name__ == "__main__":
    main()
