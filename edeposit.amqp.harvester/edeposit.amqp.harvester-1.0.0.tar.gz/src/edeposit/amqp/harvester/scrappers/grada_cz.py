#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
This module is used to download metadata from `grada.cz`.
"""
# Imports =====================================================================
import httpkie
import dhtmlparser

from utils import handle_encodnig, get_first_content, normalize_url
from utils import self_test_idiom

from ..structures import Author
from ..structures import Publication


# Variables ===================================================================
BASE_URL = "http://www.grada.cz"
URL = BASE_URL + "/novinky/?start=0&krok=100"
DOWNER = httpkie.Downloader()


# Functions & objects =========================================================
def _parse_alt_title(html_chunk):
    """
    Parse title from alternative location if not found where it should be.

    Args:
        html_chunk (obj): HTMLElement containing slice of the page with details.

    Returns:
        str: Book's title.
    """
    title = html_chunk.find(
        "input",
        {"src": "../images_buttons/objednat_off.gif"}
    )

    assert title, "Can't find alternative title!"

    title = title[0]

    assert "title" in title.params, "Can't find alternative title source!"

    # title is stored as Bleh bleh: Title
    title = title.params["title"].split(":", 1)[-1]

    return title.strip()


def _parse_title_url(html_chunk):
    """
    Parse title/name of the book and URL of the book.

    Args:
        html_chunk (obj): HTMLElement containing slice of the page with details.

    Returns:
        tuple: (title, url), both as strings.
    """
    title = html_chunk.find("div", {"class": "comment"})

    if not title:
        return _parse_alt_title(html_chunk), None

    title = title[0].find("h2")
    if not title:
        return _parse_alt_title(html_chunk), None

    # look for the url of the book if present
    url = None
    url_tag = title[0].find("a")
    if url_tag:
        url = url_tag[0].params.get("href", None)
        title = url_tag

    return title[0].getContent(), normalize_url(BASE_URL, url)


def _parse_subtitle(html_chunk):
    """
    Parse subtitle of the book.

    Args:
        html_chunk (obj): HTMLElement containing slice of the page with details.

    Returns:
        str/None: Subtitle or None if subtitle wasn't found.
    """
    subtitle = html_chunk.match(
        ["div", {"class": "comment"}],
        "h2",
        ["span", {"class": "gray"}],
    )

    return get_first_content(subtitle)


def _parse_authors(html_chunk):
    """
    Parse authors of the book.

    Args:
        html_chunk (obj): HTMLElement containing slice of the page with details.

    Returns:
        list: List of :class:`structures.Author` objects. Blank if no author \
              found.
    """
    authors = html_chunk.match(
        ["div", {"class": "comment"}],
        "h3",
        "a",
    )

    if not authors:
        return []

    authors = map(
        lambda x: Author(                            # create Author objects
            x.getContent().strip(),
            normalize_url(BASE_URL, x.params.get("href", None))
        ),
        authors
    )

    return filter(lambda x: x.name.strip(), authors)


def _parse_description(html_chunk):
    """
    Parse description of the book.

    Args:
        html_chunk (obj): HTMLElement containing slice of the page with details.

    Returns:
        str/None: Details as string with currency or None if not found.
    """
    perex = html_chunk.find("div", {"class": "perex"})

    return get_first_content(perex)


def _parse_format_pages_isbn(html_chunk):
    """
    Parse format, number of pages and ISBN.

    Args:
        html_chunk (obj): HTMLElement containing slice of the page with details.

    Returns:
        tuple: (format, pages, isbn), all as string.
    """
    ppi = get_first_content(
        html_chunk.find("div", {"class": "price-overflow"})
    )

    if not ppi:
        return None, None, None

    # all information this function should parse are at one line
    ppi = filter(lambda x: x.strip(), ppi.split("<br />"))[0]

    # parse isbn
    isbn = dhtmlparser.parseString(ppi)
    isbn = isbn.find("b")
    isbn = isbn[0].getContent() if isbn else None

    # parse pages and format
    pages = None
    book_format = None
    details = ppi.split("|")

    if len(details) >= 2:
        book_format = details[0].strip()
        pages = details[1].strip()

    return book_format, pages, isbn


def _parse_price(html_chunk):
    """
    Parse price of the book.

    Args:
        html_chunk (obj): HTMLElement containing slice of the page with details.

    Returns:
        str/None: Price as string with currency or None if not found.
    """
    price = get_first_content(
        html_chunk.find("div", {"class": "prices"})
    )

    if not price:
        return None

    # it is always in format Cena:\n150kč
    price = dhtmlparser.removeTags(price)
    price = price.split("\n")[-1]

    return price


def _process_book(html_chunk):
    """
    Parse available informations about book from the book details page.

    Args:
        html_chunk (obj): HTMLElement containing slice of the page with
                          details.

    Returns:
        obj: :class:`structures.Publication` instance with book details.
    """
    title, url = _parse_title_url(html_chunk)
    book_format, pages, isbn = _parse_format_pages_isbn(html_chunk)

    # required informations
    pub = Publication(
        title=title,
        authors=_parse_authors(html_chunk),
        price=_parse_price(html_chunk),
        publisher="Grada"
    )

    # optional informations
    pub.optionals.URL = url
    pub.optionals.ISBN = isbn
    pub.optionals.pages = pages
    pub.optionals.format = book_format
    pub.optionals.sub_title = _parse_subtitle(html_chunk)
    pub.optionals.description = _parse_description(html_chunk)

    return pub


def get_publications():
    """
    Get list of publication offered by grada.cz.

    Returns:
        list: List of :class:`.Publication` objects.
    """
    data = DOWNER.download(URL)
    dom = dhtmlparser.parseString(
        handle_encodnig(data)
    )

    book_list = dom.find("div", {"class": "item"})

    books = []
    for book in book_list:
        books.append(
            _process_book(book)
        )

    return books


def self_test():
    """
    Perform basic selftest.

    Returns:
        True: When everything is ok.

    Raises:
        AssertionError: When there is some problem.
    """
    return self_test_idiom(get_publications)
