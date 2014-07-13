#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Sends the current time to libnotify so you get a popup and notifies again at full, half oder quarterly hour.
Requires libnotify to be installed.
"""

import subprocess
import schedule
from shutil import which
from datetime import datetime
from time import sleep
from argparse import ArgumentParser


#Parse arguments
parser = ArgumentParser(
    description=__doc__)

parser.add_argument("-s", "--schedule", help="Get notified at [full] hour, [half] hour or [quarterly]. "
                                             "Defaults to quarterly", default="half")
args = parser.parse_args()


# Check if libnotify is installed
if which("notify-send") is None:
    print("Could not find notify-send. Please install libnotify.")
    exit(2)


# Get scheduled times.
arg = args.schedule
times = {
    "full": 0,
    "half": [0, 30],
    "quarterly": [0, 15, 30, 45]
}

print(times[arg])

# get time on how often to print the time
scheduler = {
    "full": 60,
    "half": 30,
    "quarterly": 15
}

print(scheduler[arg])

def get_current_min():
    cur_min = datetime.strftime(datetime.now(), "%M")
    return cur_min


def get_current_hour():
    cur_hour = datetime.strftime(datetime.now(), "%H")
    return cur_hour


def get_current_time():
    cur_time = "%s:%s" % (get_current_hour(), get_current_min())
    return cur_time


def print_time():
    print(get_current_time())
    send_message_to_notify("It is now %s" % get_current_time())


def send_message_to_notify(message):
    subprocess.call(["notify-send", message])
    return

# Print time on startup.
print_time()

while True:
    now = get_current_min()  # check for current minute
    if int(now) in times[arg]:
        schedule.every(scheduler[arg]).minutes.do(print_time)
        print_time()
        while True:
            schedule.run_pending()
            sleep(10)
    sleep(30)





