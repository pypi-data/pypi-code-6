#!/usr/bin/env python
import requests

statusURL = "http://att.mifiliberate/cgi/sysser.cgi?id=system_service&as=1&api=status"
timeout = 0.8

def network(**args):
    """Returns the name of the carrier"""
    try:
        status = requests.get(statusURL, timeout=timeout).json()
        return [{
            "contents": status['statusBarNetwork'],
            "highlight_group": ["mifi:network"]
        }]
    except requests.exceptions.RequestException:
        return None

def connectionType(**args):
    """Displays the technology used to connect, ie. EDGE, 3G, HSPA(+), LTE"""
    try:
        status = requests.get(statusURL, timeout=timeout).json()
        return [{
            "contents": status['statusBarTechnology'].split(" ")[0],
            "highlight_group": ["mifi:connectionType"]
        }]
    except requests.exceptions.RequestException:
        return None


def GPS(**args):
    """Displays the status of the GPS. ie. Off, Searching, GotFix"""
    try:
        status = requests.get(statusURL, timeout=timeout).json()
        return [{
            "contents": status['statusBarGpsStatus'].split(" ")[0],
            "highlight_group": ["mifi:GPS"]
        }]
    except requests.exceptions.RequestException:
        return None
