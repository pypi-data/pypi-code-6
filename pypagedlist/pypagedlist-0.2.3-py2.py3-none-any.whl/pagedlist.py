# -*- coding: utf-8 -*-
import abc
import math

import six


@six.add_metaclass(abc.ABCMeta)
class IPagedList(object):
    @abc.abstractproperty
    def page_count(self):
        """
        Total number of subsets within the superset.

        :rtype : int
        """

    @abc.abstractproperty
    def total_item_count(self):
        """
        Total number of objects contained within the superset.

        :rtype : int
        """

    @abc.abstractproperty
    def page_number(self):
        """
        One-based index of this subset within the superset.

        :rtype : int
        """

    @abc.abstractproperty
    def page_size(self):
        """
        Maximum size any individual subset.

        :rtype : int
        """

    @abc.abstractproperty
    def has_previous_page(self):
        """
        Returns true if this is NOT the first subset within the superset.

        :rtype : bool
        """

    @abc.abstractproperty
    def has_next_page(self):
        """
        Returns true if this is NOT the last subset within the superset.

        :rtype : bool
        """

    @abc.abstractproperty
    def is_first_page(self):
        """
        Returns true if this is the first subset within the superset.

        :rtype : bool
        """

    @abc.abstractproperty
    def is_last_page(self):
        """
        Returns true if this is the last subset within the superset.

        :rtype : bool
        """

    @abc.abstractproperty
    def first_item_on_page(self):
        """
        One-based index of the first item in the paged subset.

        :return: int
        """

    @abc.abstractproperty
    def last_item_on_page(self):
        """
        One-based index of the last item in the paged subset.

        :return: int
        """


class PagedListMetaData(IPagedList):
    def __init__(self, paged_list):
        """
        Non-enumerable version of the PagedList class.

        :type paged_list: IPagedList
        """
        self._page_count = paged_list.page_count
        self._total_item_count = paged_list.total_item_count
        self._page_number = paged_list.page_number
        self._page_size = paged_list.page_size
        self._has_previous_page = paged_list.has_previous_page
        self._has_next_page = paged_list.has_next_page
        self._is_first_page = paged_list.is_first_page
        self._is_last_page = paged_list.is_last_page
        self._first_item_on_page = paged_list.first_item_on_page
        self._last_item_on_page = paged_list.last_item_on_page

    @property
    def page_number(self):
        return self._page_number

    @property
    def is_first_page(self):
        return self._is_first_page

    @property
    def page_size(self):
        return self._page_size

    @property
    def has_previous_page(self):
        return self.has_previous_page

    @property
    def first_item_on_page(self):
        return self._first_item_on_page

    @property
    def has_next_page(self):
        return self._has_next_page

    @property
    def page_count(self):
        return self._page_count

    @property
    def last_item_on_page(self):
        return self._last_item_on_page

    @property
    def total_item_count(self):
        return self._total_item_count

    @property
    def is_last_page(self):
        return self._is_last_page


class PagedListBase(IPagedList):
    def __init__(self, query, page_number, page_size):
        assert isinstance(page_number, six.integer_types)
        assert isinstance(page_size, six.integer_types)

        if page_number < 1:
            raise IndexError("page_number cannot be below 1.")
        if page_size < 1:
            raise IndexError("page_size cannot be less than 1.")

        if not query:
            self._total_item_count = 0
        else:
            self._total_item_count = self._query_count_fn(query)
        self._page_size = page_size
        self._page_number = page_number
        if self.total_item_count > 0:
            self._page_count = int(math.ceil(self.total_item_count /
                                             float(page_size)))
        else:
            self._page_count = 0
        self._has_previous_page = page_number > 1
        self._has_next_page = page_number < self.page_count
        self._is_first_page = page_number == 1
        self._is_last_page = page_number >= self.page_count
        self._first_item_on_page = (page_number - 1) * page_size + 1
        number_of_last_item_on_page = self.first_item_on_page + page_size - 1
        if number_of_last_item_on_page > self.total_item_count:
            self._last_item_on_page = self.total_item_count
        else:
            self._last_item_on_page = number_of_last_item_on_page

        # Query subset of all items, based on current page
        if query and self.total_item_count > 0:
            if page_number == 1:
                self._subset = self._query_limit_offset_fn(query, page_size, 0)
            else:
                self._subset = self._query_limit_offset_fn(
                    query, page_size, (page_number - 1) * page_size)
        else:
            self._subset = []

    def _query_count_fn(self, query):
        return 0

    def _query_limit_offset_fn(self, query, limit, offset):
        return []

    def metadata(self):
        return PagedListMetaData(self)

    @property
    def page_number(self):
        return self._page_number

    @property
    def is_first_page(self):
        return self._is_first_page

    @property
    def page_size(self):
        return self._page_size

    @property
    def has_previous_page(self):
        return self._has_previous_page

    @property
    def first_item_on_page(self):
        return self._first_item_on_page

    @property
    def has_next_page(self):
        return self._has_next_page

    @property
    def page_count(self):
        return self._page_count

    @property
    def last_item_on_page(self):
        return self._last_item_on_page

    @property
    def total_item_count(self):
        return self._total_item_count

    @property
    def is_last_page(self):
        return self._is_last_page

    def __len__(self):
        return len(self._subset)

    def __getitem__(self, i):
        return self._subset[i]

    def __contains__(self, value):
        return value in self._subset

    def __iter__(self):
        for item in self._subset:
            yield item

    def __reversed__(self):
        for item in reversed(self._subset):
            yield item

    def index(self, value):
        return self._subset.index(value)

    def count(self, value):
        return self._subset.count(value)


class SimplePagedList(PagedListBase):
    def _query_limit_offset_fn(self, query, limit, offset):
        return query[offset:offset + limit]

    def _query_count_fn(self, query):
        return len(query)


class PagedList(PagedListBase):
    def __init__(self, query, page_number, page_size):
        """
        Initializes a new instance of the PagedList class that divides the
        supplied superset into subsets the size of the supplied pageSize.
        The instance then only containes the objects contained in the subset
        specified by index.

        :param query:  Initializes a new instance of the PagedList class that
            divides the supplied superset into subsets the size of the supplied
            page_size. The instance then only containes the objects contained
            in the subset specified by index.
        :param page_number: The one-based index of the subset of objects to be
            contained by this instance.
        :param page_size: The maximum size of any individual subset.
        :raise IndexError:
        """
        super(PagedList, self).__init__(query, page_number, page_size)

    def _query_count_fn(self, query):
        return query.count()

    def _query_limit_offset_fn(self, query, limit, offset):
        return query.limit(limit).offset(offset).all()
