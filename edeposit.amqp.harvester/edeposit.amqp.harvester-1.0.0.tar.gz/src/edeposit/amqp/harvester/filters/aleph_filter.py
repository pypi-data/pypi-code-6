#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
This module is used to skip Publications, which are already in Aleph.

Note:
    The module is using fuzzy lookup, see :func:`name_to_vector` and
    :func:`compare_names`.
"""
# Imports =====================================================================
import unicodedata

import edeposit.amqp.aleph as aleph


# Functions & objects =========================================================
def name_to_vector(name):
    """
    Convert `name` to the ASCII vector.

    Example:
        >>> name_to_vector("ing. Franta Putšálek")
        ['putsalek', 'franta', 'ing']

    Args:
        name (str): Name which will be vectorized.

    Returns:
        list: Vector created from name.
    """
    if not isinstance(name, unicode):
        name = name.decode("utf-8")

    name = name.lower()
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
    name = "".join(filter(lambda x: x.isalpha() or x == " ", list(name)))

    return sorted(name.split(), key=lambda x: len(x), reverse=True)


def compare_names(first, second):
    """
    Compare two names in complicated, but more error prone way.

    Algorithm is using vector comparison.

    Example:
        >>> compare_names("Franta Putšálek", "ing. Franta Putšálek")
        100.0
        >>> compare_names("F. Putšálek", "ing. Franta Putšálek")
        50.0

    Args:
        first (str): Fisst name as string.
        second (str): Second name as string.

    Returns:
        float: Percentage of the similarity.
    """
    first = name_to_vector(first)
    second = name_to_vector(second)

    zipped = zip(first, second)

    if not zipped:
        return 0

    similarity_factor = 0
    for fitem, _ in zipped:
        if fitem in second:
            similarity_factor += 1

    return (float(similarity_factor) / len(zipped)) * 100


def filter_publication(publication, cmp_authors=True):
    """
    Filter publications based at data from Aleph.

    Args:
        publication (obj): :class:`.Publication` instance.

    Returns:
        obj/None: None if the publication was found in Aleph or `publication` \
                  if not.
    """
    query = None
    isbn_query = False

    # there can be ISBN query or book title query
    if publication.optionals and publication.optionals.ISBN:
        query = aleph.ISBNQuery(publication.optionals.ISBN)
        isbn_query = True
    else:
        query = aleph.TitleQuery(publication.title)

    result = aleph.reactToAMQPMessage(aleph.SearchRequest(query), "")

    if not result.records:
        return publication  # book is not in database

    # if there was results with this ISBN, compare titles of the books
    # (sometimes, there are different books with same ISBN because of human
    # errors)
    if isbn_query:
        for record in result.records:
            epub = record.epublication

            # try to match title of the book
            if compare_names(epub.nazev, publication.title) >= 80:
                return None  # book already in database

        return publication

    # checks whether the details from returned EPublication match Publication's
    for record in result.records:
        epub = record.epublication

        # if the title doens't match, go to next record from aleph
        if not compare_names(epub.nazev, publication.title) >= 80:
            continue

        if not cmp_authors:
            return None  # book already in database

        # compare authors names
        for author in epub.autori:
            # convert Aleph's author structure to string
            author_str = "%s %s %s" % (
                author.firstName,
                author.lastName,
                author.title
            )

            # normalize author data from `publication`
            pub_authors = map(lambda x: x.name, publication.authors)
            if type(pub_authors) not in [list, tuple, set]:
                pub_authors = [pub_authors]

            # try to compare authors from `publication` and Aleph
            for pub_author in pub_authors:
                if compare_names(author_str, pub_author) >= 50:
                    return None  # book already in database

    return publication  # book is not in database
