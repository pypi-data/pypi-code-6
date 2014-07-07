#!/usr/bin/env python

# Name:                         local_exceptions
#
# Author: Ian Stewart
#
# TODO:
#	- Find all instances of raising EmptyMethod rather than EmptyMethod() and fix them.
#
#    vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
#    Copyright (C) 2014  Ian M Stewart
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    For the GNU General Public License, see <http://www.gnu.org/licenses/>.
#    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# History (version, date, change author):
#
#	2014-05-14	IMS/AIfA
#.......................................................................
# * ims_exceptions.py copied to this release version, renamed, and all but relevant code removed.
#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

"""This contains several commonly-used exceptions."""

_module_name = 'local_exceptions'

#.......................................................................
class ExceededMaxNumIter(Exception):
  def __init__(self, maxNumIter):
    self.maxNumIter = maxNumIter
  def __str__(self):
    return 'Maximum permitted number of iterations %d exceeded.' % (self.maxNumIter)

class EmptyMethod(Exception):
  def __str__(self):
    return 'This method should be implemented in a subclass.'

class FailedTest(Exception):
  def __init__(self, test):
    self.test = test
  def __str__(self):
    return 'Failed test %s' % (self.test)

class GracefulStop(Exception):
  def __init__(self, gracefulStopFile):
    self.gracefulStopFile = gracefulStopFile
  def __str__(self):
    return 'Graceful stop file %s is present.' % (self.gracefulStopFile)

class NonmatchingShapes(Exception):
  def __init__(self, shape1, name1, shape2, name2):
    self.shape1 = shape1
    self.shape2 = shape2
    self.name1 = name1
    self.name2 = name2
  def __str__(self):
    return "Shape %s for array %s doesn't match shape %s for array %s." % (str(self.shape1), self.name1, str(self.shape2), self.name2)

class NotYetImplemented(Exception): pass
#  def __str__(self):
#    return "This choice is not yet implemented."

class ObsoleteModule(Exception):
  def __init__(self, name):
    self.moduleName = name

  def __str__(self):
    return 'This module %s is obsolete. Please use a later one.' % (self.moduleName)

class OutOfRange(Exception):
  def __init__(self, rangeObject, arg):
    self.rangeObject = rangeObject
    self.arg = arg
  def __str__(self):
    return 'Argument %f was outside the range %s.' % (self.arg, self.rangeObject)

class Report(Exception):
  def __init__(self, message):
    self.message = message
  def __str__(self):
    return self.message

class Bug(Report):
  def __init__(self, message):
    Report.__init__(self, 'Bug! '+message)

class ShellCommandFailed(Report):
  def __init__(self, message):
    Report.__init__(self, message)

class TestStop(Exception):
  def __str__(self):
    return 'Stopping here for test purposes.'

class UnrecognizedChoiceObject(Exception):
  def __init__(self, choiceObject, message=None):
    self.choiceObject = choiceObject
    self.message = message
  def __str__(self):
    if self.message==None:
      return 'Choice %s was not recognized.' % (str(self.choiceObject))
    else:
      return '%s: choice %s was not recognized.' % (self.message, str(self.choiceObject))


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
  raise NotYetImplemented()
