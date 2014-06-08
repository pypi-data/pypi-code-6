#!/usr/bin/env python
# -*- coding: utf-8 -*-


class EqualityMixin(object):

    def __eq__(self, other):
        if type(other) is type(self):
            return (self.__dict__ == other.__dict__)
        return NotImplemented

    def __ne__(self, other):
        return not self.__eq__(other)

# vim: filetype=python
