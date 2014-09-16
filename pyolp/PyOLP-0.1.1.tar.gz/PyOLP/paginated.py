#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (C) 2013, Cameron White
#                                                                              
# PyGithub is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.                                                           
#                                                                              
# PyGithub is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS   
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#                                                                      
# You should have received a copy of the GNU Lesser General Public License
# along with PyGithub. If not, see <http://www.gnu.org/licenses/>.

class PaginatedList():

    def __init__(self, contentClass, requester, uri, parameters=None):

        self.__requester = requester
        self.__contentClass = contentClass
        self.__uri = uri
        self.__parameters = parameters
        
        self.__getFirstPage()

    def _applyContentClass(self, element):
        return self.__contentClass(
            self.__requester, self.__headers, element)

    def _isBiggerThan(self, index):
        return len(self.__elements) > index or self.__couldGrow()

    def __couldGrow(self):
        if self.__next is None:
            return False
        else:
            return True

    def __fetchToIndex(self, index):
        while len(self.__elements) <= index and self.__couldGrow():
            self.__grow()

    def __getFirstPage(self):
        
        headers, data = self.__requester.requestJsonAndCheck(
                self.__uri,
                self.__parameters
        )

        self.__elements = self.__parse(headers, data)

    def __getitem__(self, index):
        assert isinstance(index, (int, slice))
        if isinstance(index, (int, long)):
            self.__fetchToIndex(index)
            return self.__elements[index]
        else:
            return self._Slice(self, index)
    
    def __getNextPage(self):

        headers, data = self.__requester.requestJsonAndCheck(
                self.__next
        )

        return self.__parse(headers, data)

    def __grow(self):
        newElements = self.__getNextPage()
        self.__elements += newElements
        return newElements

    def __iter__(self):
        
        for element in self.__elements:
            yield self.__contentClass(
                    self.__requester, self.__headers, element)
        while self.__couldGrow():
            self.__grow()
            for element in self.__elements:
                yield self._applyContentClass(element)

    def __parse(self, headers, data):

        self.__headers = headers
        meta = data["meta"]
        self.__limit = meta["limit"]
        self.__next = meta["next"]
        self.__offset = meta["offset"]
        self.__previous = meta["previous"]
        self.__total_count = meta["total_count"]

        return data["objects"]

    class _Slice:
        def __init__(self, theList, theSlice):
            self.__list = theList
            self.__start = theSlice.start or 0
            self.__stop = theSlice.stop
            self.__step = theSlice.step or 1

        def __iter__(self):
            index = self.__start
            while not self.__finished(index):
                if self.__list._isBiggerThan(index):
                    yield self.__list._applyContentClass(self.__list[index])
                    index += self.__step
                else:
                    return

        def __finished(self, index):
            return self.__stop is not None and index >= self.__stop
