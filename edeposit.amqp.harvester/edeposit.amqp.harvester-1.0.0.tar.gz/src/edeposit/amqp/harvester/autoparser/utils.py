#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
This module contains number of functions, which are used at multiple places in
autoparser.
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


def content_matchs(tag_content, content_transformer=None):
    """
    Generate function, which checks whether the content of the tag matchs
    `tag_content`.

    Args:
        tag_content (str): Content of the tag which will be matched thru whole
                           DOM.
        content_transformer (fn, default None): Function used to transform all
                            tags before matching.

    Returns:
        bool: True for every matching tag.

    Note:
        This function can be used as parameter for ``.find()`` method in
        HTMLElement.
    """
    def content_matchs_closure(element):
        if not element.isTag():
            return False

        cont = element.getContent()
        if content_transformer:
            cont = content_transformer(cont)

        return tag_content == cont

    return content_matchs_closure


def is_equal_tag(element, tag_name, params, content):
    """
    Check is `element` object match rest of the parameters.

    All checks are performed only if proper attribute is set in the HTMLElement.

    Args:
        element (obj): HTMLElement instance.
        tag_name (str): Tag name.
        params (dict): Parameters of the tag.
        content (str): Content of the tag.

    Returns:
        bool: True if everyhing matchs, False otherwise.
    """
    if tag_name and tag_name != element.getTagName():
        return False

    if params and not element.containsParamSubset(params):
        return False

    if content is not None and content.strip() != element.getContent().strip():
        return False

    return True


def has_neigh(tag_name, params=None, content=None, left=True):
    """
    This function generates functions, which matches all tags with neighbours
    defined by parameters.

    Args:
        tag_name (str): Tag has to have neighbour with this tagname.
        params (dict): Tag has to have neighbour with this parameters.
        params (str): Tag has to have neighbour with this content.
        left (bool, default True): Tag has to have neigbour on the left, or
                                   right (set to ``False``).

    Returns:
        bool: True for every matching tag.

    Note:
        This function can be used as parameter for ``.find()`` method in
        HTMLElement.
    """
    def has_neigh_closure(element):
        if not element.parent \
           or not (element.isTag() and not element.isEndTag()):
            return False

        # filter only visible tags/neighbours
        childs = element.parent.childs
        childs = filter(
            lambda x: (x.isTag() and not x.isEndTag()) \
                      or x.getContent().strip() or x is element,
            childs
        )
        if len(childs) <= 1:
            return False

        ioe = childs.index(element)
        if left and ioe > 0:
            return is_equal_tag(childs[ioe - 1], tag_name, params, content)

        if not left and ioe + 1 < len(childs):
            return is_equal_tag(childs[ioe + 1], tag_name, params, content)

        return False

    return has_neigh_closure
