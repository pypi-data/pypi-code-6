#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Binh Vu <binh@toan2.com>"

from .logger.logger import Logger

def getlogger(ns):
	return Logger(ns, level=Logger.DEBUG)