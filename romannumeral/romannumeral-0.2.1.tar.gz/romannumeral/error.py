# -*- coding: utf-8 -*-

class RomanError(Exception):
	pass


class ParseError(RomanError):
	pass


class OutOfRangeError(RomanError):
	pass
