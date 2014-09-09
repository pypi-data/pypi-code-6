#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
This module is used to download last 100 books published by `ben.cz`.
"""
# Imports =====================================================================
import httpkie
import dhtmlparser

from utils import self_test_idiom

from ..structures import Author
from ..structures import Publication


# Variables ===================================================================
URL = "http://shop.ben.cz/"  #: Base url of the eshop.
URL += r"Produkty.aspx?lang=cz&nak=BEN+-+technick%u00e1+literatura"
DOWNER = httpkie.Downloader()
DOWNER.cookies = {
    "shop.ben.cz": {
        "pageSize": "100",
        "viewProductSize": "tabulka"
    }
}


# Functions & objects =========================================================
def _get_last_td(el):
    """
    Return last <td> found in `el` DOM.

    Args:
        el (obj): :class:`dhtmlparser.HTMLElement` instance.

    Returns:
        obj: HTMLElement instance if found, or None if there are no <td> tags.
    """
    if not el:
        return None

    if type(el) in [list, tuple, set]:
        el = el[0]

    last = el.find("td")

    if not last:
        return None

    return last[-1]


def _get_td_or_none(details, ID):
    """
    Get <tr> tag with given `ID` and return content of the last <td> tag from
    <tr> root.

    Args:
        details (obj): :class:`dhtmlparser.HTMLElement` instance.
        ID (str): id property of the <tr> tag.

    Returns:
        str: Content of the last <td> as strign.
    """
    content = details.find("tr", {"id": ID})
    content = _get_last_td(content)

    # if content is None, return it
    if not content:
        return None

    content = content.getContent().strip()

    # if content is blank string, return None
    if not content:
        return None

    return content


# Parsers =====================================================================
def _parse_title(dom, details):
    """
    Parse title/name of the book.

    Args:
        dom (obj): HTMLElement containing whole HTML page.
        details (obj): HTMLElement containing slice of the page with details.

    Returns:
        str: Book's title.

    Raises:
        AssertionError: If title not found.
    """
    title = details.find("h1")

    # if the header is missing, try to parse title from the <title> tag
    if not title:
        title = dom.find("title")
        assert title, "Can't find <title> tag!"

        return title[0].getContent().split("|")[0].strip()

    return title[0].getContent().strip()


def _parse_authors(details):
    """
    Parse authors of the book.

    Args:
        details (obj): HTMLElement containing slice of the page with details.

    Returns:
        list: List of :class:`structures.Author` objects. Blank if no author \
              found.
    """
    authors = details.find(
        "tr",
        {"id": "ctl00_ContentPlaceHolder1_tblRowAutor"}
    )

    if not authors:
        return []  # book with unspecified authors

    # parse authors from HTML and convert them to Author objects
    author_list = []
    for author in authors[0].find("a"):
        author_obj = Author(author.getContent())

        if "href" in author.params:
            author_obj.URL = author.params["href"]

        author_list.append(author_obj)

    return author_list


def _parse_publisher(details):
    """
    Parse publisher of the book.

    Args:
        details (obj): HTMLElement containing slice of the page with details.

    Returns:
        str/None: Publisher's name as string or None if not found.
    """
    publisher = _get_td_or_none(
        details,
        "ctl00_ContentPlaceHolder1_tblRowNakladatel"
    )

    # publisher is not specified
    if not publisher:
        return None

    publisher = dhtmlparser.removeTags(publisher).strip()

    # return None instead of blank string
    if not publisher:
        return None

    return publisher


def _parse_price(details):
    """
    Parse price of the book.

    Args:
        details (obj): HTMLElement containing slice of the page with details.

    Returns:
        str/None: Price as string with currency or None if not found.
    """
    price = _get_td_or_none(
        details,
        "ctl00_ContentPlaceHolder1_tblRowBeznaCena"
    )

    return price


def _parse_pages_binding(details):
    """
    Parse number of pages and binding of the book.

    Args:
        details (obj): HTMLElement containing slice of the page with details.

    Returns:
        (pages, binding): Tuple with two string or two None.
    """
    pages = _get_td_or_none(
        details,
        "ctl00_ContentPlaceHolder1_tblRowRozsahVazba"
    )

    if not pages:
        return None, None

    binding = None  # binding info and number of pages is stored in same string
    if "/" in pages:
        binding = pages.split("/")[1].strip()
        pages = pages.split("/")[0].strip()

    if not pages:
        pages = None

    return pages, binding


def _parse_ISBN_EAN(details):
    """
    Parse ISBN and EAN.

    Args:
        details (obj): HTMLElement containing slice of the page with details.

    Returns:
        (ISBN, EAN): Tuple with two string or two None.
    """
    isbn_ean = _get_td_or_none(
        details,
        "ctl00_ContentPlaceHolder1_tblRowIsbnEan"
    )

    if not isbn_ean:
        return None, None

    ean = None
    isbn = None
    if "/" in isbn_ean:  # ISBN and EAN are stored in same string
        isbn, ean = isbn_ean.split("/")
        isbn = isbn.strip()
        ean = ean.strip()
    else:
        isbn = isbn_ean.strip()

    if not isbn:
        isbn = None

    return isbn, ean


def _parse_edition(details):
    """
    Parse edition (vydání) of the book.

    Args:
        details (obj): HTMLElement containing slice of the page with details.

    Returns:
        str/None: Edition as string with currency or None if not found.
    """
    edition = _get_td_or_none(
        details,
        "ctl00_ContentPlaceHolder1_tblRowVydani"
    )

    return edition


def _parse_description(details):
    """
    Parse description of the book.

    Args:
        details (obj): HTMLElement containing slice of the page with details.

    Returns:
        str/None: Details as string with currency or None if not found.
    """
    description = details.find("div", {"class": "detailPopis"})

    # description not found
    if not description:
        return None

    # remove links to ebook version
    ekniha = description[0].find("div", {"class": "ekniha"})
    if ekniha:
        ekniha[0].replaceWith(dhtmlparser.HTMLElement(""))

    # remove links to other books from same cathegory
    detail = description[0].find("p", {"class": "detailKat"})
    if detail:
        detail[0].replaceWith(dhtmlparser.HTMLElement(""))

    # remove all HTML elements
    description = dhtmlparser.removeTags(description[0]).strip()

    # description is blank
    if not description:
        return None

    return description


def _process_book(book_url):
    """
    Parse available informations about book from the book details page.

    Args:
        book_url (str): Absolute URL of the book.

    Returns:
        obj: :class:`structures.Publication` instance with book details.
    """
    data = DOWNER.download(book_url)
    dom = dhtmlparser.parseString(data)

    details_tags = dom.find("div", {"id": "contentDetail"})

    assert details_tags, "Can't find details of the book."

    details = details_tags[0]

    # parse required informations
    title = _parse_title(dom, details)
    authors = _parse_authors(details)
    publisher = _parse_publisher(details)
    price = _parse_price(details)
    pages, binding = _parse_pages_binding(details)

    pub = Publication(
        title,
        authors,
        price,
        publisher
    )

    # parse optional informations
    pub.optionals.URL = book_url
    pub.optionals.binding = binding

    pub.optionals.pages = pages
    pub.optionals.ISBN, pub.optionals.EAN = _parse_ISBN_EAN(details)
    pub.optionals.edition = _parse_edition(details)
    pub.optionals.description = _parse_description(details)

    return pub


def get_publications():
    """
    Get list of publication offered by ben.cz.

    Returns:
        list: List of :class:`structures.Publication` objects.
    """
    data = DOWNER.download(URL)
    dom = dhtmlparser.parseString(data)

    book_list = dom.find("div", {"class": "seznamKniha"})

    assert book_list, "Can't find <div> with class 'seznamKniha'!"

    books = []
    for html_chunk in book_list:
        a = html_chunk.find("a")

        assert a, "Can't find link to the details of the book!"

        if a[0].find("span", {"class": "ruzek pripravujeme"}):
            continue

        books.append(
            _process_book(a[0].params["href"])
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
