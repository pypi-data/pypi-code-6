# -*- coding: utf-8 -*-
from time import sleep
import random

from termcolor import colored


def main():
    colors = ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    highlights = ['on_grey', 'on_red', 'on_green', 'on_yellow', 'on_blue', 'on_magenta', 'on_cyan', 'on_white']
    attributes = ['bold', 'dark', 'underline', 'blink', 'reverse', 'concealed']


    while True:
        print(colored('beats', random.choice(colors), random.choice(highlights), attrs=[random.choice(attributes)]))
        sleep(0.25)
