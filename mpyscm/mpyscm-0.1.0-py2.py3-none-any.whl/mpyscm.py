# -*- coding: utf-8 -*-

__author__ = 'Abdullah Al Mamun'
__email__ = 'mamunabms@yahoo.com'
__version__ = '0.1.0'


# mpyscm.py
import getpass


# Define the main function of our program
def main():
    user = getpass.getuser()
    config = '/home/' + user + '/.ssh/config'
    entries = open(config, 'r').readlines()
    return entries

if __name__ == "__main__":
    out = main()
    print out
