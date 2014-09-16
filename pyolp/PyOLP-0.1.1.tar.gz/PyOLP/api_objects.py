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

from . import api_exceptions
from .requester import Requester
import datetime

class _NotSetType:
    def __repr__(self):
        return "NotSet"

    value = None
NotSet = _NotSetType()

class _ValuedAttribute:
    def __init__(self, value):
        self.value = value

class _BadAttribute:
    def __init__(self, value, expectedType, exception=None):
        self.__value = value
        self.__expectedType = expectedType
        self.__exception = exception

    @property
    def value(self):
        raise api_exceptions.BadAttributeException(self.__value, self.__expectedType)

class ApiObject(object):

    def __init__(self, requester, headers, attributes):
        self._requester = requester
        self._initAttributes() # virtual
        self._storeAndUseAttributes(headers, attributes)
    
    def _storeAndUseAttributes(self, headers, attributes):
        # Make sure headers are assigned before calling _useAttributes
        # (Some derived classes will use headers in _useAttributes)
        self._headers = headers
        self._rawData = attributes
        self._useAttributes(attributes) # virtual

    @staticmethod
    def __makeSimpleAttribute(value, type):
        if value is None or isinstance(value, type):
            return _ValuedAttribute(value)
        else:
            return _BadAttribute(value, type)

    @staticmethod
    def _makeStringAttribute(value):
        return ApiObject.__makeSimpleAttribute(value, (str, unicode))

    @staticmethod
    def _makeIntAttribute(value):
        return ApiObject.__makeSimpleAttribute(value, (int, long))

    @staticmethod
    def _makeBoolAttribute(value):
        return ApiObject.__makeSimpleAttribute(value, bool)

    @staticmethod
    def _makeFloatAttribute(value):
        try:
            value = float(value)
        except ValueError:
            pass
        return ApiObject.__makeSimpleAttribute(value, float)

    @staticmethod
    def _makeDatetimeAttribute(value):
        try:
            d = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            d = datetime.datetime.strptime(value, "%Y-%m-%d")
        return ApiObject.__makeSimpleAttribute(d, datetime.datetime)

    @property
    def raw_data(self):
        """
        :type: dict
        """
        return self._rawData

    @property
    def raw_headers(self):
        """
        :type: dict
        """
        return self._headers

    def update(self):

        status, responseHeaders, output = self._requester.requestJson(
             self._resource_uri.value # virtual
        )

        headers, data = self._requester._Requester__check(status, responseHeaders, output)
        self._storeAndUseAttributes(headers, data)
    
class Price(ApiObject):

    @property
    def amount(self):
        """
        :type: float
        """
        return self._amount.value

    @property
    def created_at(self):
        """
        :type: datetime
        """
        return self._created_at.value

    @property
    def effective_date(self):
        """
        :type: datetime
        """
        return self._effective_date.value

    @property
    def id(self):
        """
        :type: string
        """
        return self._id.value
    
    @property
    def modified_at(self):
        """
        :type: datetime
        """
        return self._modified_at.value

    @property
    def product(self):
        """
        :type: related
        """
        return self._product.value

    @property
    def resource_uri(self):
        """
        :type: string
        """
        return self._resource_uri.value
    
    def get_product(self):

        headers, data = self._requester.requestJsonAndCheck(
            self.product
        )
        return Product(self._requester, headers, data)

    def _initAttributes(self):
        self._amount = NotSet
        self._created_at = NotSet
        self._effective_date = NotSet
        self._id = NotSet
        self._modified_at = NotSet
        self._product = NotSet
        self._resource_uri = NotSet

    def _useAttributes(self, attributes):
        if "amount" in attributes:
            self._amount = self._makeFloatAttribute(attributes["amount"])
        if "created_at" in attributes:
            self._created_at = self._makeDatetimeAttribute(attributes["created_at"])
        if "effective_date" in attributes:
            self._effective_date = self._makeDatetimeAttribute(attributes["effective_date"])
        if "id" in attributes:
            self._id = self._makeStringAttribute(attributes["id"])
        if "modified_at" in attributes:
            self._modified_at = self._makeDatetimeAttribute(attributes["modified_at"])
        if "product" in attributes:
            self._product = self._makeStringAttribute(attributes["product"])
        if "resource_uri" in attributes:
            self._resource_uri = self._makeStringAttribute(attributes["resource_uri"])

class Product(ApiObject):

    @property
    def age(self):
        """
        :type: float
        """
        return self._age.value

    @property
    def bottles_per_case(self):
        """
        :type: int
        """
        return self._bottles_per_case.value

    @property
    def code(self):
        """
        :type: string
        """
        return self._code.value

    @property
    def created_at(self):
        """
        :type: datetime
        """
        return self._created_at.value
    
    @property
    def description(self):
        """
        :type: string
        """
        return self._description.value

    @property
    def id(self):
        """
        :type: string
        """
        return self._id.value

    @property
    def modified_at(self):
        """
        :type: datetime
        """
        return self._modified_at.value

    @property
    def on_sale(self):
        """
        :type: bool
        """
        return self._on_sale.value

    @property
    def proof(self):
        """
        :type: float
        """
        return self._proof.value
    
    @property
    def resource_uri(self):
        """
        :type: string
        """
        return self._resource_uri.value

    @property
    def size(self):
        """
        :type: string
        """
        return self._size.value

    @property
    def slug(self):
        """
        :type: string
        """
        return self._slug.value

    @property
    def status(self):
        """
        :type: string
        """
        return self._status.value

    @property
    def title(self):
        """
        :type: string
        """
        return self._title.value

    def get_price(self):

        headers, data = self._requester.requestJsonAndCheck(
            '/api/v1/price/' + str(self.id) + '/'
        )
        return Price(self._requester, headers, data)

    def _initAttributes(self):
        self._age = NotSet
        self._bottles_per_case = NotSet
        self._code = NotSet
        self._created_at = NotSet
        self._description = NotSet
        self._id = NotSet
        self._modified_at = NotSet
        self._on_sale = NotSet
        self._proof = NotSet
        self._resource_uri = NotSet
        self._size = NotSet
        self._slug = NotSet
        self._status = NotSet
        self._title = NotSet

    def _useAttributes(self, attributes):
        if "age" in attributes:
            self._age = self._makeFloatAttribute(attributes["age"])
        if "bottles_per_case" in attributes:
            self._bottles_per_case = self._makeIntAttribute(attributes["bottles_per_case"])
        if "code" in attributes:
            self._code = self._makeStringAttribute(attributes["code"])
        if "created_at" in attributes:
            self._created_at = self._makeDatetimeAttribute(attributes["created_at"])
        if "description" in attributes:
            self._description = self._makeStringAttribute(attributes["description"])
        if "id" in attributes:
            self._id = self._makeStringAttribute(attributes["id"])
        if "modified_at" in attributes:
            self._modified_at = self._makeDatetimeAttribute(attributes["modified_at"])
        if "on_sale" in attributes:
            self._on_sale = self._makeBoolAttribute(attributes["on_sale"])
        if "proof" in attributes:
            self._proof = self._makeFloatAttribute(attributes["proof"])
        if "resource_uri" in attributes:
            self._resource_uri = self._makeStringAttribute(attributes["resource_uri"])
        if "size" in attributes:
            self._size = self._makeStringAttribute(attributes["size"])
        if "slug" in attributes:
            self._slug = self._makeStringAttribute(attributes["slug"])
        if "status" in attributes:
            self._status = self._makeStringAttribute(attributes["status"])
        if "title" in attributes:
            self._title = self._makeStringAttribute(attributes["title"])

class Store(ApiObject):

    @property
    def address(self):
        """
        :type: string
        """
        return self._address.value

    @property
    def address_raw(self):
        """
        :type: string
        """
        return self._address_raw.value

    @property
    def county(self):
        """
        :type: string
        """
        return self._county.value

    @property
    def hours_raw(self):
        """
        :type: string
        """
        return self._hours_raw.value

    @property
    def id(self):
        """
        :type: string
        """
        return self._id.value
    
    @property
    def key(self):
        """
        :type: int
        """
        return self._key.value
    
    @property
    def latitude(self):
        """
        :type: float
        """
        return self._latitude.value
    
    @property
    def longitude(self):
        """
        :type: float
        """
        return self._longitude.value

    @property
    def name(self):
        """
        :type: string
        """
        return self._name.value

    @property
    def phone(self):
        """
        :type: string
        """
        return self._phone.value

    @property
    def resource_uri(self):
        """
        :type: string
        """
        return self._resource_uri.value

    def _initAttributes(self):
        self._address = NotSet
        self._address_raw = NotSet
        self._county = NotSet
        self._hours_raw = NotSet
        self._id = NotSet
        self._key = NotSet
        self._latitude = NotSet
        self._longitude = NotSet
        self._name = NotSet
        self._phone = NotSet
        self._resource_uri = NotSet

    def _useAttributes(self, attributes):
        if "address" in attributes:
            self._address = self._makeStringAttribute(attributes["address"])
        if "address_raw" in attributes:
            self._address_raw = self._makeStringAttribute(attributes["address_raw"])
        if "county" in attributes:
            self._county = self._makeStringAttribute(attributes["county"])
        if "hours_raw" in attributes:
            self._hours_raw = self._makeStringAttribute(attributes["hours_raw"])
        if "id" in attributes:
            self._id = self._makeStringAttribute(attributes["id"])
        if "key" in attributes:
            self._key = self._makeIntAttribute(attributes["key"])
        if "latitude" in attributes:
            self._latitude = self._makeFloatAttribute(attributes["latitude"])
        if "longitude" in attributes:
            self._longitude = self._makeFloatAttribute(attributes["longitude"])
        if "name" in attributes:
            self._name = self._makeStringAttribute(attributes["name"])
        if "phone" in attributes:
            self._phone = self._makeStringAttribute(attributes["phone"])
        if "resource_uri" in attributes:
            self._resource_uri = self._makeStringAttribute(attributes["resource_uri"])
