#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
This module contains number of functions, which are used in the rest of the
scrappers submodule.
"""
# Imports =====================================================================
import dhtmlparser


# Functions & objects =========================================================
def _get_encoding(dom, default="utf-8"):
    """
    Try to look for meta tag in given `dom`.

    Args:
        dom (obj): pyDHTMLParser dom of HTML elements.
        default (default "utr-8"): What to use if encoding is not found in
                                   `dom`.

    Returns:
        str/default: Given encoding or `default` parameter if not found.
    """
    encoding = dom.find("meta", {"http-equiv": "Content-Type"})

    if not encoding:
        return default

    encoding = encoding[0].params.get("content", None)

    if not encoding:
        return default

    return encoding.lower().split("=")[-1]


def handle_encodnig(html):
    """
    Look for encoding in given `html`. Try to convert `html` to utf-8.

    Args:
        html (str): HTML code as string.

    Returns:
        str: HTML code encoded in UTF.
    """
    encoding = _get_encoding(
        dhtmlparser.parseString(
            html.split("</head>")[0]
        )
    )

    if encoding == "utf-8":
        return html

    return html.decode(encoding).encode("utf-8")


def get_first_content(el_list, alt=None, strip=True):
    """
    Return content of the first element in `el_list` or `alt`. Also return `alt`
    if the content string of first element is blank.

    Args:
        el_list (list): List of HTMLElement objects.
        alt (default None): Value returner when list or content is blank.
        strip (bool, default True): Call .strip() to content.

    Returns:
        str or alt: String representation of the content of the first element \
                    or `alt` if not found.
    """
    if not el_list:
        return alt

    content = el_list[0].getContent()

    if strip:
        content = content.strip()

    if not content:
        return alt

    return content


def is_absolute_url(url, protocol="http"):
    """
    Test whether `url` is absolute url (``http://domain.tld/something``) or
    relative (``../something``).

    Args:
        url (str): Tested string.
        protocol (str, default "http"): Protocol which will be seek at the
                 beginning of the `url`.

    Returns:
        bool: True if url is absolute, False if not.
    """
    if ":" not in url:
        return False

    protocol, rest = url.split(":", 1)

    if protocol.startswith(protocol) and rest.startswith("//"):
        return True

    return False


def normalize_url(base_url, rel_url):
    """
    Normalize the `url` - from relative, create absolute URL.

    Args:
        base_url (str): Domain with ``protocol://`` string
        rel_url (str): Relative or absolute url.

    Returns:
        str/None: Normalized URL or None if `url` is blank.
    """
    if not rel_url:
        return None

    if not is_absolute_url(rel_url):
        rel_url = rel_url.replace("../", "/")

        if (not base_url.endswith("/")) and (not rel_url.startswith("/")):
            return base_url + "/" + rel_url.replace("../", "/")

        return base_url + rel_url.replace("../", "/")

    return rel_url


def has_param(param):
    """
    Generate function, which will check `param` is in html element.

    This function can be used as parameter for .find() method in HTMLElement.
    """
    def has_param_closure(element):
        """
        Look for `param` in `element`.
        """
        if element.params.get(param, "").strip():
            return True

        return False

    return has_param_closure


def must_contain(tag_name, tag_content, container_tag_name):
    """
    Generate function, which checks if given element contains `tag_name` with
    string content `tag_content` and also another tag named
    `container_tag_name`.

    This function can be used as parameter for .find() method in HTMLElement.
    """
    def must_contain_closure(element):
        # containing in first level of childs <tag_name> tag
        matching_tags = element.match(tag_name, absolute=True)
        if not matching_tags:
            return False

        # which's content match `tag_content`
        if matching_tags[0].getContent() != tag_content:
            return False

        # and also contains <container_tag_name> tag
        if container_tag_name and \
           not element.match(container_tag_name, absolute=True):
            return False

        return True

    return must_contain_closure


def content_matchs(tag_content, content_transformer=None):
    """
    Generate function, which checks whether the content of the tag matchs
    `tag_content`.

    Args:
        tag_content (str): Content of the tag which will be matched thru whole
                           DOM.
        content_transformer (fn, default None): Function used to transform all
                            tags before matching.

    This function can be used as parameter for .find() method in HTMLElement.
    """
    def content_matchs_closure(element):
        if not element.isTag():
            return False

        cont = element.getContent()
        if content_transformer:
            cont = content_transformer(cont)

        return tag_content == cont

    return content_matchs_closure


def self_test_idiom(fn):
    """
    Perform basic selftest.

    Returns:
        True: When everything is ok.

    Raises:
        AssertionError: When there is some problem.
    """
    books = fn()

    assert len(books) > 0

    for book in books:
        error = "Book doesn't have all required parameters!\n"
        error += str(book.to_namedtuple())

        assert book.title, error
        assert book.authors is not None, error  # can be blank
        assert book.price, error
        assert book.publisher, error

        if book.optionals.ISBN:
            assert len(book.optionals.ISBN) >= 10

        if book.optionals.URL:
            protocol, rest = book.optionals.URL.split(":", 1)

            assert protocol.startswith("http")
            assert rest.startswith("//")

    return True
