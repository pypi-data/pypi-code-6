# -*- coding: utf-8 -*-

# Copyright 2013 Vincent Jacques
# vincent@vincent-jacques.net

# This file is part of MockMockMock. http://jacquev6.github.com/MockMockMock

# MockMockMock is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# MockMockMock is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with MockMockMock.  If not, see <http://www.gnu.org/licenses/>.

from MockException import MockException
from Expectation import Expectation
import ArgumentChecking


class AnyAttribute:
    def __init__(self, apply):
        self.__apply = apply

    def __getattr__(self, name):
        # @todo Fix this hack
        # Hack to allow m.expect._call_.withArguments,
        # because m.expect.__call__.withArguments fails,
        # because function doesn't have attribute "withArguments"
        if name == "_call_":
            name = "__call__"
        # End of hack
        if name == "__dir__":
            raise AttributeError()
        return self.__apply(name)

    def __call__(self, *args, **kwds):  # Needed to make isinstance(mock.expect, collections.Callable) return True
        return self.__getattr__("__call__")(*args, **kwds)


class CallChecker:
    def __init__(self, handler, expectations):
        self.__handler = handler
        self.__expectations = expectations

    def __call__(self, *args, **kwds):
        return self.__handler.checkExpectationCall(self.__expectations, args, kwds)


class BasicExpectationProxy:
    def __init__(self, expectation):
        self.__expectation = expectation

    def andReturn(self, value):
        return self.andExecute(lambda: value)

    def andRaise(self, exception):
        def Raise():
            raise exception
        return self.andExecute(Raise)

    def andExecute(self, action):
        self.__expectation.setAction(action)
        return None


class CallableExpectationProxy(BasicExpectationProxy):
    def __init__(self, expectation):
        BasicExpectationProxy.__init__(self, expectation)
        self.__expectation = expectation

    def __call__(self, *args, **kwds):
        return self.withArguments(ArgumentChecking.Equality(args, kwds))

    def withArguments(self, checker):
        self.__expectation.expectCall(checker)
        return BasicExpectationProxy(self.__expectation)


class CallRecorder:
    def __init__(self, handler, mockName, attrName, realObject):
        self.__handler = handler
        self.__mockName = mockName
        self.__attrName = attrName
        self.__realObject = realObject

    def __call__(self, *args, **kwds):
        try:
            ret = self.__realObject(*args, **kwds)
            self.__handler.addRecordedCall({
                "object": self.__mockName,
                "attribute": self.__attrName,
                "arguments": args,
                "keywords": kwds,
                "return": ret,
            })
            return ret
        except Exception, e:
            self.__handler.addRecordedCall({
                "object": self.__mockName,
                "attribute": self.__attrName,
                "arguments": args,
                "keywords": kwds,
                "exception": e,
            })
            raise


class ExpectationHandler(object):
    def __init__(self, initialGroup):
        self.__currentGroup = initialGroup
        self.__recordedCalls = []
        self.__objects = {}

    # expect
    def expect(self, mockName):
        return AnyAttribute(lambda attrName: self.addExpectation(mockName + "." + attrName))

    def addExpectation(self, name):
        # Note that accepting name == "__call__" allows the mock object to be callable with no specific code
        expectation = Expectation(name)
        self.__currentGroup.addExpectation(expectation)
        return CallableExpectationProxy(expectation)

    def pushGroup(self, group):
        self.__currentGroup.addGroup(group)
        self.__currentGroup = group
        return self.StackPoper(self)

    class StackPoper:
        def __init__(self, handler):
            self.__handler = handler

        def __enter__(self):
            pass

        def __exit__(self, *ignored):
            self.__handler.popGroup()

    def popGroup(self):
        self.__currentGroup = self.__currentGroup.parent

    # call
    def object(self, mockName):
        # @todo Test this objects cache. It's important because it gives the same *identity* to all calls to mock.object
        # @todo Detect if client tries to create several mocks with same name
        o = self.__objects.get(mockName)
        if o is None:
            o = AnyAttribute(lambda attrName: self.checkExpectation(mockName + "." + attrName))
            self.__objects[mockName] = o
        return o

    def checkExpectation(self, calledName):
        possibleExpectations = self.__currentGroup.getCurrentPossibleExpectations()
        goodNamedExpectations = [expectation for expectation in possibleExpectations if expectation.checkName(calledName)]

        if len(goodNamedExpectations) == 0:
            # @todo if possibleExpectations is empty, adapt message
            # @todo display arguments
            raise MockException(calledName + " called instead of " + " or ".join(e.name for e in possibleExpectations))

        allGoodNamedExpectationsExpectNoCall = not any(expectation.expectsCall() for expectation in goodNamedExpectations)
        allGoodNamedExpectationsExpectCall = all(expectation.expectsCall() for expectation in goodNamedExpectations)

        if allGoodNamedExpectationsExpectCall:
            return CallChecker(self, goodNamedExpectations)
        elif allGoodNamedExpectationsExpectNoCall:
            return self.__callExpectation(goodNamedExpectations[0])
        else:
            raise MockException(calledName + " is expected as a property and as a method call in an unordered group")

    def checkExpectationCall(self, expectations, args, kwds):
        for expectation in expectations:
            if expectation.checkCall(args, kwds):
                return self.__callExpectation(expectation)
        raise MockException(expectations[0].name + " called with bad arguments " + str(args) + " " + str(kwds))

    def __callExpectation(self, expectation):
        returnValue, self.__currentGroup = expectation.call()
        return returnValue

    def tearDown(self):
        if self.__currentGroup.requiresMoreCalls():
            raise MockException(" or ".join(self.__currentGroup.getRequiredCallsExamples()) + " not called")

    # record / replay
    def record(self, mockName, realObject):
        return AnyAttribute(lambda attrName: self.recordCall(realObject, mockName, attrName))

    def recordCall(self, realObject, mockName, attrName):
        try:
            attr = getattr(realObject, attrName)
            if callable(attr):
                return CallRecorder(self, mockName, attrName, attr)
            else:
                self.addRecordedCall({
                    "object": mockName,
                    "attribute": attrName,
                    "return": attr,
                })
                return attr
        except Exception, e:
            self.addRecordedCall({
                "object": mockName,
                "attribute": attrName,
                "exception": e,
            })
            raise

    def addRecordedCall(self, call):
        self.__recordedCalls.append(call)

    def getRecordedCalls(self):
        return self.__recordedCalls
