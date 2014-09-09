#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
This module is used to download metadata informations from `cpress.cz`.
"""
# Imports =====================================================================
import httpkie
import dhtmlparser

from utils import handle_encodnig, get_first_content, normalize_url, has_param
from utils import must_contain, self_test_idiom

from ..structures import Author
from ..structures import Publication


# Variables ===================================================================
BASE_URL = "http://www.cpress.cz/"
URL = BASE_URL + "/novinky/"
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
    title = html_chunk.find("img", fn=has_param("alt"))

    if not title:
        raise UserWarning("Can't find alternative title source!")

    return title[0].params["alt"].strip()


def _parse_alt_url(html_chunk):
    """
    Parse URL from alternative location if not found where it should be.

    Args:
        html_chunk (obj): HTMLElement containing slice of the page with details.

    Returns:
        str: Book's URL.
    """
    url_list = html_chunk.find("a", fn=has_param("href"))
    url_list = map(lambda x: x.params["href"], url_list)
    url_list = filter(lambda x: not x.startswith("autori/"), url_list)

    if not url_list:
        return None

    return normalize_url(BASE_URL, url_list[0])


def _parse_title_url(html_chunk):
    """
    Parse title/name of the book and URL of the book.

    Args:
        html_chunk (obj): HTMLElement containing slice of the page with details.

    Returns:
        tuple: (title, url), both as strings.
    """
    url = None
    title_tags = html_chunk.match(
        ["div", {"class": "polozka_nazev"}],
        ["a", None, has_param("href")]
    )

    if not title_tags:
        return _parse_alt_title(html_chunk), _parse_alt_url(html_chunk)

    title = title_tags[0]

    url = normalize_url(BASE_URL, title.params["href"])
    title = title.getContent()

    if not title:
        title = _parse_alt_title(html_chunk)

    return title, url


def _parse_authors(html_chunk):
    """
    Parse authors of the book.

    Args:
        html_chunk (obj): HTMLElement containing slice of the page with details.

    Returns:
        list: List of :class:`structures.Author` objects. Blank if no author \
              found.
    """
    authors_tags = html_chunk.match(
        ["div", {"class": "polozka_autor"}],
        "a"
    )

    authors = []
    for author_tag in authors_tags:
        # get name
        name = author_tag.getContent().strip()

        # skip tags without name
        if not name:
            continue

        # get url - if not found, set it to None
        url = author_tag.params.get("href", None)
        if url:
            url = normalize_url(BASE_URL, url)

        authors.append(
            Author(name, url)
        )

    return authors


def _parse_price(html_chunk):
    """
    Parse price of the book.

    Args:
        html_chunk (obj): HTMLElement containing slice of the page with details.

    Returns:
        str/None: Price as string with currency or None if not found.
    """
    price = html_chunk.find("span", {"class": "cena"})

    if not price:
        raise UserWarning("Price not found!")

    return get_first_content(price)


def _parse_from_table(html_chunk, what):
    """
    Go thru table data in `html_chunk` and try to locate content of the
    neighbor cell of the cell containing `what`.

    Returns:
        str: Table data or None.
    """
    ean_tag = html_chunk.find("tr", fn=must_contain("th", what, "td"))

    if not ean_tag:
        return None

    return get_first_content(ean_tag[0].find("td"))


def _parse_ean(html_chunk):
    """
    Parse EAN.

    Args:
        html_chunk (obj): HTMLElement containing slice of the page with details.

    Returns:
        str/None: EAN as string or None if not found.
    """
    return _parse_from_table(html_chunk, "EAN:")


def _parse_date(html_chunk):
    """
    Parse date.

    Args:
        html_chunk (obj): HTMLElement containing slice of the page with details.

    Returns:
        str/None: date as string or None if not found.
    """
    return _parse_from_table(html_chunk, "Datum vydání:")


def _parse_format(html_chunk):
    """
    Parse format.

    Args:
        html_chunk (obj): HTMLElement containing slice of the page with details.

    Returns:
        str/None: Format as string or None if not found.
    """
    return _parse_from_table(html_chunk, "Formát:")


def _parse_description(html_chunk):
    """
    Parse description of the book.

    Args:
        html_chunk (obj): HTMLElement containing slice of the page with details.

    Returns:
        str/None: Description as string or None if not found.
    """
    description_tag = html_chunk.match(
        ["div", {"class": "kniha_detail_text"}],
        "p"
    )

    if not description_tag:
        return None

    description = get_first_content(description_tag)
    description = description.replace("<br />", "\n")
    description = description.replace("<br/>", "\n")

    return dhtmlparser.removeTags(description).strip()


def _process_book(html_chunk):
    """
    Parse available informations about book from the book details page.

    Args:
        html_chunk (obj): HTMLElement containing slice of the page with details.

    Returns:
        obj: :class:`structures.Publication` instance with book details.
    """
    title, book_url = _parse_title_url(html_chunk)

    # download page with details
    data = DOWNER.download(book_url)
    dom = dhtmlparser.parseString(
        handle_encodnig(data)
    )
    details = dom.find("div", {"id": "kniha_detail"})[0]

    # required parameters
    pub = Publication(
        title=title,
        authors=_parse_authors(html_chunk),
        price=_parse_price(details),
        publisher="CPress"
    )

    # optional parameters
    pub.optionals.URL = book_url
    pub.optionals.EAN = _parse_ean(details)
    pub.optionals.format = _parse_format(details)
    pub.optionals.pub_date = _parse_date(details)
    pub.optionals.description = _parse_description(details)

    return pub


def get_publications():
    """
    Get list of publication offered by cpress.cz.

    Returns:
        list: List of :class:`.Publication` objects.
    """
    data = DOWNER.download(URL)
    dom = dhtmlparser.parseString(
        handle_encodnig(data)
    )

    book_list = dom.find("div", {"class": "polozka"})

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
