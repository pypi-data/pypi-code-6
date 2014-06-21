#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is part of formv and is released under the MIT License: 
# http://www.opensource.org/licenses/mit-license.php 

from formv.validators.base import VRange
from formv.exception import Invalid
from formv.utils import extract_text as _

__all__ = ('VFloat','VInteger','VNumber',)

class VInteger(VRange):
    def _validate(self, value):        
        self.messages.update({'invalid': _('Not an integer value')})

        try:
            return VRange._validate(self, int(value))
        except:
            raise Invalid(self.message('invalid'), value)


class VFloat(VRange):
    def _validate(self, value):
        self.messages.update({'invalid': _('Not a floating point value')})

        try:
            return VRange._validate(self, float(value))
        except:
            raise Invalid(self.message('invalid'), value)


class VNumber(VRange):
    def _validate(self, value):
        self.messages.update({'invalid': _('Please enter a number')})

        try: 
            value = VRange._validate(self, float(value))
            try:
                int_value = int(value)
            except OverflowError:
                int_value = None
            if value == int_value:
                return int_value
            return value
        except ValueError:
            raise Invalid(self.message('invalid'), value)