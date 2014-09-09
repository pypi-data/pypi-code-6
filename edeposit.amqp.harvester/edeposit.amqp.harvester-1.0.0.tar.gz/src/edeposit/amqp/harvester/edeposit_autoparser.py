#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import sys
import os.path
import argparse

import dhtmlparser

import autoparser.utils as utils
import autoparser.conf_reader as conf_reader
import autoparser.vectors as vectors
import autoparser.path_patterns as path_patterns
import autoparser.generator as generator
from autoparser.path_patterns import PathCall, Chained


# Functions & objects =========================================================
def _create_dom(data):
    """
    Creates doublelinked DOM from `data`.

    Args:
        data (str/HTMLElement): Either string or HTML element.

    Returns:
        obj: HTMLElement containing double linked DOM.
    """
    if not isinstance(data, dhtmlparser.HTMLElement):
        data = dhtmlparser.parseString(
            utils.handle_encodnig(data)
        )

    dhtmlparser.makeDoubleLinked(data)

    return data


def _locate_element(dom, el_content, transformer=None):
    """
    Find element containing `el_content` in `dom`. Use `transformer` function
    to content of all elements in `dom` in order to correctly transforming them
    to match them with `el_content`.

    Args:
        dom (obj): HTMLElement tree.
        el_content (str): Content of element will be picked from `dom`.
        transformer (fn, default None): Transforming function.

    Note:
        `transformer` parameter can be for example simple lambda::

            lambda x: x.strip()

    Returns:
        list: Matching HTMLElements.
    """
    return dom.find(
        None,
        fn=utils.content_matchs(el_content, transformer)
    )


def _match_elements(dom, matches):
    """
    Find location of elements matching patterns specified in `matches`.

    Args:
        dom (obj): HTMLElement DOM tree.
        matches (dict): Structure: ``{"var": {"data": "match", ..}, ..}``.

    Returns:
        dict: Structure: ``{"var": {"data": HTMLElement_obj, ..}, ..}``
    """
    out = {}
    for key, content in matches.items():
        pattern = content["data"].strip()
        if "\n" in pattern:
            pattern = pattern.split()
            transformer = lambda x: x.strip().split()
        else:
            transformer = lambda x: x.strip()

        matching_elements = _locate_element(
            dom,
            pattern,
            transformer=transformer
        )

        not_found_msg = content.get("notfoundmsg", "").replace("$name", key)
        if not not_found_msg.strip():
            not_found_msg = "Can't locate variable '%s' with content '%s'!" % (
                key,
                pattern,
            )
        content["notfoundmsg"] = not_found_msg

        # in case of multiple elements, find only elements with propert tagname
        tagname = content.get("tagname", "").strip().lower()
        if tagname:
            matching_elements = filter(
                lambda x: x.getTagName().strip().lower() == tagname,
                matching_elements
            )

        if not matching_elements:
            raise UserWarning(not_found_msg)

        if len(matching_elements) > 1:
            raise UserWarning(
                "Ambigious content '%s'!" % content
                + "Content was found in multiple elements!"
            )

        out[key] = matching_elements[0]

    return out


def _collect_paths(element):
    """
    Collect all possible path which leads to `element`.

    Function returns standard path from root element to this, reverse path,
    which uses negative indexes for path, also some pattern matches, like
    "this is element, which has neighbour with id 7" and so on.

    Args:
        element (obj): HTMLElement instance.

    Returns:
        list: List of :class:`.PathCall` and :class:`.Chained` objects.
    """
    output = []

    # look for element by parameters - sometimes the ID is unique
    path = vectors.el_to_path_vector(element)
    root = path[0]
    params = element.params if element.params else None
    match = root.find(element.getTagName(), params)

    if len(match) == 1:
        output.append(
            PathCall("find", 0, [element.getTagName(), params])
        )

    # look for element by neighbours
    output.extend(path_patterns.neighbours_pattern(element))

    # look for elements by patterns - element, which parent has tagname, and
    # which parent has tagname ..
    output.extend(path_patterns.predecesors_pattern(element, root))

    index_backtrack = []
    last_index_backtrack = []
    params_backtrack = []
    last_params_backtrack = []

    # look for element by paths from root to element
    for el in reversed(path):
        # skip root elements
        if not el.parent:
            continue

        tag_name = el.getTagName()
        match = el.parent.wfind(tag_name).childs
        index = match.index(el)

        index_backtrack.append(
            PathCall("wfind", index, [tag_name])
        )
        last_index_backtrack.append(
            PathCall("wfind", index - len(match), [tag_name])
        )

        # if element has some parameters, use them for lookup
        if el.params:
            match = el.parent.wfind(tag_name, el.params).childs
            index = match.index(el)

            params_backtrack.append(
                PathCall("wfind", index, [tag_name, el.params])
            )
            last_params_backtrack.append(
                PathCall("wfind", index - len(match), [tag_name, el.params])
            )
        else:
            params_backtrack.append(
                PathCall("wfind", index, [tag_name])
            )
            last_params_backtrack.append(
                PathCall("wfind", index - len(match), [tag_name])
            )

    output.extend([
        Chained(reversed(params_backtrack)),
        Chained(reversed(last_params_backtrack)),
        Chained(reversed(index_backtrack)),
        Chained(reversed(last_index_backtrack)),
    ])

    return output


def _is_working_path(dom, path, element):
    """
    Check whether the path is working or not.

    Aply proper search function interpreting `path` to `dom` and check, if
    returned object is `element`. If so, return ``True``, otherwise ``False``.

    Args:
        dom (obj): HTMLElement DOM.
        path (obj): :class:`.PathCall` Instance containing informations about
                    path and which function it require to obtain element the
                    path is pointing to.
        element (obj): HTMLElement instance used to decide whether `path`
                       points to correct `element` or not.

    Returns:
        bool: True if `path` correctly points to proper `element`.
    """
    def i_or_none(el, i):
        """
        Return ``el[i]`` if the list is not blank, or None otherwise.

        Args:
            el (list, tuple): Any indexable object.
            i (int): Index.

        Returns:
            obj: Element at index `i` if `el` is not blank, or ``None``.
        """
        if not el:
            return None

        return el[i]

    # map decoders of all paths to one dictionary to make easier to call them
    path_functions = {
        "find": lambda el, index, params:
            i_or_none(el.find(*params), index),
        "wfind": lambda el, index, params:
            i_or_none(el.wfind(*params).childs, index),
        "match": lambda el, index, params:
            i_or_none(el.match(*params), index),
        "left_neighbour_tag": lambda el, index, neigh_data:
            i_or_none(
                el.find(
                    neigh_data.tag_name,
                    neigh_data.params,
                    fn=utils.has_neigh(*neigh_data.fn_params, left=True)
                ),
                index
            ),
        "right_neighbour_tag": lambda el, index, neigh_data:
            i_or_none(
                el.find(
                    neigh_data.tag_name,
                    neigh_data.params,
                    fn=utils.has_neigh(*neigh_data.fn_params, left=False)
                ),
                index
            ),
    }

    # call all decoders and see what you get from them
    el = None
    if isinstance(path, PathCall):
        el = path_functions[path.call_type](dom, path.index, path.params)
    elif isinstance(path, Chained):
        for path in path.chain:
            dom = path_functions[path.call_type](dom, path.index, path.params)
            if not dom:
                return False
        el = dom
    else:
        raise UserWarning(
            "Unknown type of path parameters! (%s)" % str(path)
        )

    if not el:
        return False

    # test whether returned item is the item we are looking for
    return el.getContent().strip() == element.getContent().strip()


def select_best_paths(examples):
    """
    Process `examples`, select only paths that works for every example. Select
    best paths with highest priority.

    Args:
        examples (dict): Output from :func:`.read_config`.

    Returns:
        list: List of :class:`.PathCall` and :class:`.Chained` objects.
    """
    possible_paths = {}  # {varname: [paths]}

    # collect list of all possible paths to all existing variables
    for example in examples:
        dom = _create_dom(example["html"])
        matching_elements = _match_elements(dom, example["vars"])

        for key, match in matching_elements.items():
            if key not in possible_paths:  # TODO: merge paths together?
                possible_paths[key] = _collect_paths(match)

    # leave only paths, that works in all examples where, are required
    for example in examples:
        dom = _create_dom(example["html"])
        matching_elements = _match_elements(dom, example["vars"])

        for key, paths in possible_paths.items():
            if key not in matching_elements:
                continue

            possible_paths[key] = filter(
                lambda path: _is_working_path(
                    dom,
                    path,
                    matching_elements[key]
                ),
                paths
            )

    priorities = [
        "find",
        "left_neighbour_tag",
        "right_neighbour_tag",
        "wfind",
        "match",
        "Chained"
    ]
    priorities = dict(map(lambda x: (x[1], x[0]), enumerate(priorities)))

    # sort all paths by priority table
    for key in possible_paths.keys():
        possible_paths[key] = list(sorted(
            possible_paths[key],
            key=lambda x: priorities.get(x.call_type, 100)
        ))

    return possible_paths


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Autoparser - parser generator."
    )
    parser.add_argument(
        "-c",
        "--config",
        required=True,
        help="""YAML Configuration file used to specify paths to data and
                matches, which will be used to create generator."""
    )

    args = parser.parse_args()

    if not os.path.exists(args.config):
        sys.stderr.write("Can't open '%s'!\n" % args.config)
        sys.exit(1)

    config = conf_reader.read_config(args.config)

    if not config:
        sys.stderr.write("Configuration file '%s' is blank!\n" % args.config)
        sys.exit(1)

    paths = select_best_paths(config)
    print generator.generate_parsers(config, paths)
