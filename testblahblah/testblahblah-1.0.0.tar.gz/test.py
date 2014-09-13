#!/usr/bin/python

"""Still don't get why they chose to call simple files by another name,
who the fuck does that?"""

def test_lol(thelist):
    for value in thelist:
        if isinstance(value, list):
            test_lol(value)
        else:
            print(value)

"""This is the end of this file called module for no fucking reason"""
