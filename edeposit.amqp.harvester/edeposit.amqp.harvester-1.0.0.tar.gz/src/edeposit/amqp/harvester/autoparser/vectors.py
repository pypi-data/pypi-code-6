#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
This module contains functions to convert `DOM` relations to `path-like` lists
of elements defined by tag names and parameters.
"""
# Imports =====================================================================


# Functions & objects =========================================================
def el_to_path_vector(el):
    """
    Convert `el` to vector of foregoing elements.

    Attr:
        el (obj): Double-linked HTMLElement instance.

    Returns:
        list: HTMLElements which considered as path from root to `el`.
    """
    path = []
    while el.parent:
        path.append(el)
        el = el.parent

    return list(reversed(path + [el]))


def common_vector_root(vec1, vec2):
    """
    Return common root of the two vectors.

    Args:
        vec1 (list/tuple): First vector.
        vec2 (list/tuple): Second vector.

    Usage example::

        >>> common_vector_root([1, 2, 3, 4, 5], [1, 2, 8, 9, 0])
        [1, 2]

    Returns:
        list: Common part of two vectors or blank list.
    """
    root = []
    for v1, v2 in zip(vec1, vec2):
        if v1 == v2:
            root.append(v1)
        else:
            return root

    return root


def find_common_root(elements):
    """
    Find root which is common for all `elements`.

    Args:
        elements (list): List of double-linked HTMLElement objects.

    Returns:
        list: Vector of HTMLElement containing path to common root.
    """
    if not elements:
        raise UserWarning("Can't find common root - no elements suplied.")

    root_path = el_to_path_vector(elements.pop())

    for el in elements:
        el_path = el_to_path_vector(el)

        root_path = common_vector_root(root_path, el_path)

        if not root_path:
            raise UserWarning(
                "Vectors without common root:\n%s" % str(el_path)
            )

    return root_path
