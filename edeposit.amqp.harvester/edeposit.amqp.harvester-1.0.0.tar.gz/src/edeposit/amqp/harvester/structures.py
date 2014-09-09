#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
This module contains all structures used in AMQP communication.
"""
# Imports =====================================================================
from collections import namedtuple


# Functions & objects =========================================================
class Author(object):
    """
    Author name representation.

    Attributes:
        name (str): String containing author's name.
        URL (str): URL to author's profile.
    """
    def __init__(self, name, URL=None):
        self.name = name
        self.URL = URL

    def to_namedtuple(self):
        """
        Convert class to namedtuple.

        Note:
            This method is neccessary for AMQP communication.

        Returns:
            namedtuple: Representation of the class as simple structure.
        """
        keys = filter(lambda x: not x.startswith("_"), self.__dict__)
        opt_nt = namedtuple(self.__class__.__name__, keys)
        filtered_dict = dict(map(lambda x: (x, self.__dict__[x]), keys))

        return opt_nt(**filtered_dict)

    def __str__(self):
        return self.name


class Optionals(object):
    """
    Structure for holding optional informations about given publication.

    Note:
        This structure is usually used as container inside
        :attr:`Publication.optionals`.

    Attributes:
        sub_title (str, default None):  Subtitle of the book.
        format (str, default None): Format of the book - A5 for example.
        pub_date (str, default None): Date when the book was published.
        pub_place (str, default None): Name of the city, where the book was
                                       published.
        ISBN (str, default None): ISBN of the book.
        description (str, default None): Description of the book, which may
                    contain HTML tags and elements!
        pages (str, default None): Number of pages.
        EAN (str, default None): EAN of the book.
        language (str, default None): Language of the book.
        edition (str, default None): Edition in which the book was published.
        URL (str, default None): URL to the eshop with the book.
        binding (str, default None): Binding of the book (`brožovaná` for
                                     example).
        is_ebook (bool, default False): If True, metadata belongs to ebook.
    """
    def __init__(self):
        self.sub_title = None
        self.format = None
        self.pub_date = None
        self.pub_place = None
        self.ISBN = None
        self.description = None
        self.pages = None
        self.EAN = None
        self.language = None
        self.edition = None  # vydání
        self.URL = None
        self.binding = None
        self.is_ebook = False

        self._any_set = False
        self._all_set = True

    def __setattr__(self, key, val):
        if "_all_set" in self.__dict__ and key not in self.__dict__:
            raise ValueError(
                "%s has no attribute %s!" % (self.__class__.__name__, key)
            )

        if not key.startswith("_") and val is not None:
            self.__dict__["_any_set"] = True

        self.__dict__[key] = val

    def to_namedtuple(self):
        """
        Convert class to namedtuple.

        Note:
            This method is neccessary for AMQP communication.

        Returns:
            namedtuple: Representation of the class as simple structure.
        """
        keys = filter(lambda x: not x.startswith("_"), self.__dict__)
        opt_nt = namedtuple(self.__class__.__name__, keys)
        filtered_dict = dict(map(lambda x: (x, self.__dict__[x]), keys))

        return opt_nt(**filtered_dict)


class Publication(object):
    """
    This class contains only required minimal subset of informations about
    `publication`.

    Attributes:
        title (str): Title of the book.
        price (str): Price as string with currency.
        publisher (str): Publishers name as string.
        authors (list): List of :class:`Author` objects. May be blank.
        optionals (obj): Reference to :class:`Optionals` object with optional
                         informations.
    """
    def __init__(self, title, authors, price, publisher):
        self.title = title
        self.price = price
        self.publisher = publisher

        if type(authors) in [str, unicode]:
            self.authors = [Author(authors)]
        elif type(authors) not in [list, set, tuple]:
            self.authors = [authors]
        else:
            self.authors = authors

        self.optionals = Optionals()

        self._all_set = True

    def to_namedtuple(self):
        """
        Convert class and all subclasses (:class:`Author`, :class:`Optionals`)
        to namedtuple.

        Note:
            This method is neccessary for AMQP communication.

        Returns:
            namedtuple: Representation of the class as simple structure.
        """
        keys = filter(lambda x: not x.startswith("_"), self.__dict__)
        opt_nt = namedtuple(self.__class__.__name__, keys)

        filt_dict = dict(map(lambda x: (x, self.__dict__[x]), keys))

        # convert Author objects to namedtuple
        authors = []
        for author in filt_dict["authors"]:
            authors.append(author.to_namedtuple())

        filt_dict["authors"] = authors

        # convert optionals to namedtuple if set, or to None if not
        if filt_dict["optionals"]._any_set:
            filt_dict["optionals"] = filt_dict["optionals"].to_namedtuple()
        else:
            filt_dict["optionals"] = None

        return opt_nt(**filt_dict)

    def _get_hash(self):
        """
        Create hash of the class.

        Hash should be unique for given ebook, so ISBN is main component of the
        hash if provided.

        Returns:
            str: Hash.
        """
        if self.optionals and self.optionals.ISBN:
            isbn = self.optionals.ISBN.replace("-", "")

            if len(isbn) <= 10:
                return "97880" + isbn

            return isbn

        if self.optionals and self.optionals.EAN:
            return self.optionals.EAN

        return self.title + ",".join(map(lambda x: x.name, self.authors))

    def __setattr__(self, key, val):
        if "_all_set" in self.__dict__ and key not in self.__dict__:
            raise ValueError(
                "%s has no attribute %s!" % (self.__class__.__name__, key)
            )

        self.__dict__[key] = val

    def __hash__(self):
        return hash(self._get_hash())

    def __eq__(self, other):
        if not other:
            return False

        keys = filter(
            lambda x: not x.startswith("_") and x != "optionals",
            self.__dict__
        )

        for key in keys:
            if getattr(self, key) != getattr(other, key):
                return False

        return True


class Publications(namedtuple("Publication", ["publications"])):
    """
    AMQP communication structured used to hold the transfered informations.

    Attributes:
        publications (list): List of :class:`Publication` namedtuples.
    """
    pass
